import { ArgumentError, AuthRequiredError, CommandExecutionError, EmptyResultError, TimeoutError } from '@jackwener/opencli/errors';
import { cli } from '@jackwener/opencli/registry';
import { unwrapEvaluateResult } from './_shared/evaluate-result.js';
import { gotoInstagramHome } from './_shared/navigation.js';

const INSTAGRAM_TIMELINE_FIELD = 'xdt_api__v1__feed__user_timeline_graphql_connection';
const INSTAGRAM_USERNAME_RE = /^(?=.*[A-Za-z0-9_])[A-Za-z0-9._]{1,30}$/;
const INSTAGRAM_MEDIA_ID_RE = /^\d+(_\d+)?$/;
const INSTAGRAM_CAPTURE_TIMEOUT_MS = 20000;
const INSTAGRAM_MAX_PAGINATION_PAGES = 5;
const INSTAGRAM_MEDIA_TYPES = new Map([[1, 'photo'], [2, 'video'], [8, 'carousel']]);
const INSTAGRAM_DRIFT_HINT = 'The response shape changed; the adapter needs updating.';

function requirePage(page) {
    if (!page)
        throw new CommandExecutionError('Browser session required for instagram user');
    return page;
}

function normalizeInstagramLimit(kwargs) {
    const limit = kwargs.limit;
    if (!Number.isInteger(limit) || limit < 1) {
        throw new ArgumentError(`Invalid limit: ${kwargs.limit}`, 'Expected a positive integer, for example: opencli instagram user nasa --limit 5');
    }
    return limit;
}

function normalizeInstagramUsername(kwargs) {
    const username = String(kwargs.username ?? '').trim().replace(/^@/, '');
    if (!INSTAGRAM_USERNAME_RE.test(username)) {
        throw new ArgumentError(`Invalid Instagram username: ${kwargs.username}`, 'Expected letters, digits, periods or underscores, for example: opencli instagram user nasa');
    }
    return username;
}

function readMediaId(node, index) {
    const id = node.pk ?? node.id;
    if ((typeof id !== 'string' && typeof id !== 'number') || !INSTAGRAM_MEDIA_ID_RE.test(String(id))) {
        throw new CommandExecutionError(`Instagram timeline edge #${index + 1} carried no usable media id`, INSTAGRAM_DRIFT_HINT);
    }
    return String(id);
}

function mapTimelineNode(node, index) {
    const type = INSTAGRAM_MEDIA_TYPES.get(node.media_type);
    if (!type) {
        throw new CommandExecutionError(`Instagram post #${index + 1} returned unsupported media_type ${node.media_type}`, INSTAGRAM_DRIFT_HINT);
    }
    return {
        index: index + 1,
        caption: (node.caption?.text || '').replace(/\n/g, ' ').substring(0, 100),
        likes: node.like_count ?? 0,
        comments: node.comment_count ?? 0,
        type,
        date: node.taken_at ? new Date(node.taken_at * 1000).toLocaleDateString() : '',
    };
}

/**
 * Runs inside the fresh Instagram document (embedded via `.toString()`).
 * Instagram streams PolarisProfileTimelineQuery over /graphql/query as
 * newline-delimited JSON chunks, which OpenCLI's single-JSON interceptor fails
 * to parse. Observe /graphql/ XHR+fetch in-page cleanly and restore hooks.
 */
async function captureInstagramTimelineInPage(username, limit, timeoutMs, maxPages, timelineField) {
    const rawResponses = [];
    const proto = XMLHttpRequest.prototype;
    const originalOpen = proto.open;
    const originalSend = proto.send;
    const originalFetch = window.fetch;
    proto.open = function (method, url) {
        this.__opencliUrl = String(url);
        return originalOpen.apply(this, arguments);
    };
    proto.send = function () {
        if (/graphql/.test(this.__opencliUrl || '')) {
            this.addEventListener('load', () => rawResponses.push(String(this.responseText || '')));
        }
        return originalSend.apply(this, arguments);
    };
    window.fetch = async function (input) {
        const response = await originalFetch.apply(this, arguments);
        const url = typeof input === 'string' ? input : (input && input.url) || '';
        if (/graphql/.test(url)) {
            response.clone().text().then((text) => rawResponses.push(text), () => {});
        }
        return response;
    };

    const parseChunks = (text) => {
        const payloads = [];
        for (const line of String(text).split('\n')) {
            const clean = line.trim().replace(/^for \(;;\);/, '');
            if (!clean) continue;
            try { payloads.push(JSON.parse(clean)); } catch { /* ignore non-JSON framing */ }
        }
        return payloads;
    };
    const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

    const connections = [];
    let graphqlError = '';
    const drain = () => {
        while (rawResponses.length) {
            for (const payload of parseChunks(rawResponses.shift())) {
                if (Array.isArray(payload?.errors) && payload.errors.length && !graphqlError) {
                    graphqlError = String(payload.errors[0].message || payload.errors[0].summary || 'GraphQL error');
                }
                const conn = payload?.data?.[timelineField];
                if (conn && typeof conn === 'object') {
                    connections.push(conn);
                }
            }
        }
    };

    try {
        if (!/(?:^|;\s*)ds_user_id=/.test(document.cookie)) return { kind: 'auth' };
        history.pushState({}, '', '/' + encodeURIComponent(username) + '/');
        window.dispatchEvent(new PopStateEvent('popstate', { state: {} }));
        const deadline = Date.now() + timeoutMs;
        while (Date.now() < deadline) {
            await sleep(250);
            drain();
            if (connections.length > 0) break;
            if (/sorry, this page isn.t available/i.test((document.body && (document.body.innerText || document.body.textContent)) || '')) {
                return { kind: 'not-found' };
            }
        }
        if (connections.length === 0) {
            return { kind: 'no-timeline', error: graphqlError };
        }
        let collected = connections.reduce((acc, c) => acc + (Array.isArray(c.edges) ? c.edges.length : 0), 0);
        let lastInfo = connections[connections.length - 1]?.page_info ?? null;
        let pages = 0;
        while (collected < limit && lastInfo?.has_next_page && pages < maxPages) {
            const prevCount = connections.length;
            window.scrollTo(0, document.body.scrollHeight);
            const pageDeadline = Date.now() + timeoutMs;
            while (Date.now() < pageDeadline) {
                await sleep(300);
                drain();
                if (connections.length > prevCount) break;
            }
            if (connections.length === prevCount) break;
            collected = connections.reduce((acc, c) => acc + (Array.isArray(c.edges) ? c.edges.length : 0), 0);
            lastInfo = connections[connections.length - 1]?.page_info ?? null;
            pages += 1;
        }
        return { kind: 'ok', pathname: window.location.pathname, connections, graphqlError };
    } catch (caught) {
        return { kind: 'exception', detail: String((caught && caught.message) || caught) };
    } finally {
        proto.open = originalOpen;
        proto.send = originalSend;
        window.fetch = originalFetch;
    }
}

cli({
    site: 'instagram',
    name: 'user',
    access: 'read',
    description: 'Get recent posts from an Instagram user',
    domain: 'www.instagram.com',
    args: [
        { name: 'username', required: true, positional: true, help: 'Instagram username' },
        { name: 'limit', type: 'int', default: 12, help: 'Number of posts' },
    ],
    columns: ['index', 'caption', 'likes', 'comments', 'type', 'date'],
    browser: true,
    navigateBefore: false,
    func: async (page, kwargs) => {
        const browserPage = requirePage(page);
        const username = normalizeInstagramUsername(kwargs);
        const limit = normalizeInstagramLimit(kwargs);
        await gotoInstagramHome(browserPage, true);
        const script = `(${captureInstagramTimelineInPage.toString()})(${JSON.stringify(username)}, ${limit}, ${INSTAGRAM_CAPTURE_TIMEOUT_MS}, ${INSTAGRAM_MAX_PAGINATION_PAGES}, ${JSON.stringify(INSTAGRAM_TIMELINE_FIELD)})`;
        let result;
        for (let attempt = 0; attempt < 2 && !result; attempt++) {
            try {
                result = unwrapEvaluateResult(await browserPage.evaluate(script));
            } catch {
                if (attempt === 1) {
                    throw new CommandExecutionError('Instagram page request failed (network or browser context)', 'Check the Instagram page and retry after any temporary restriction clears.');
                }
            }
        }
        if (!result || typeof result !== 'object') {
            throw new CommandExecutionError('Instagram returned an invalid timeline capture result');
        }
        if (result.kind === 'auth') {
            throw new AuthRequiredError('www.instagram.com', 'Not logged in to Instagram (no ds_user_id cookie in this browser session)');
        }
        if (result.kind === 'not-found') {
            throw new EmptyResultError(`instagram user ${username}`, `Instagram has no account named ${username}, or it is not visible to this session.`);
        }
        if (result.kind === 'exception') {
            throw new CommandExecutionError(`Instagram timeline read failed: ${result.detail}`);
        }
        if (result.kind === 'no-timeline') {
            if (result.error) {
                throw new CommandExecutionError(`Instagram GraphQL error: ${result.error}`, 'Wait before retrying or check the session.');
            }
            throw new CommandExecutionError(`Instagram returned no timeline response for ${username}`, 'The profile may be private or unavailable, or you may need to log in to Instagram.');
        }
        if (typeof result.pathname === 'string' && result.pathname.toLowerCase() !== `/${username.toLowerCase()}/`) {
            throw new CommandExecutionError(`Could not route to /${username}/ (still on ${result.pathname})`);
        }
        const nodes = [];
        const seen = new Set();
        for (const conn of result.connections || []) {
            if (!Array.isArray(conn.edges)) {
                throw new CommandExecutionError(`Instagram timeline response for ${username} had no edges array`, INSTAGRAM_DRIFT_HINT);
            }
            conn.edges.forEach((edge, idx) => {
                const node = edge?.node;
                if (!node || typeof node !== 'object') {
                    throw new CommandExecutionError(`Instagram timeline edge #${idx + 1} carried no media node`, INSTAGRAM_DRIFT_HINT);
                }
                const id = readMediaId(node, idx);
                if (seen.has(id)) return;
                seen.add(id);
                nodes.push(node);
            });
        }
        if (nodes.length === 0) {
            throw new EmptyResultError('instagram user', `${username} has no visible posts`);
        }
        return nodes.slice(0, limit).map(mapTimelineNode);
    },
});
