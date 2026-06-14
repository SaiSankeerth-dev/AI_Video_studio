# Push `multi-agent-video-editor` to GitHub

The repo is already committed (full history) inside **`ai-video-studio.zip`** and
**`ai-video-studio.bundle`** in this folder. Use one of the routes below.

> ⚠️ Don't run git inside `AI_VE` itself — it's OneDrive-synced and git's `.git` files get
> locked (that's why the automated push failed). Work from a folder **outside OneDrive**, e.g.
> `C:\Users\V. Sai Sankeerth\Projects\`.

---

## Route A — command line, from the ZIP  (recommended)

1. Extract `ai-video-studio.zip` to a non-OneDrive folder, e.g.
   `C:\Users\V. Sai Sankeerth\Projects\`  → gives `...\Projects\ai-video-studio\` (already a git repo).
2. On GitHub: **New repository** → owner `SaiSankeerth-dev`, name **`multi-agent-video-editor`**,
   **do NOT** add a README/.gitignore/license (keep it empty), Create.
3. In a terminal:

```bash
cd "C:\Users\V. Sai Sankeerth\Projects\ai-video-studio"
git remote add origin https://github.com/SaiSankeerth-dev/multi-agent-video-editor.git
git branch -M main
git push -u origin main
```

Git/your credential manager (or GitHub Desktop's login) handles auth in the browser.

---

## Route B — from the BUNDLE (single-file repo, no unzip)

```bash
cd "C:\Users\V. Sai Sankeerth\Projects"
git clone "C:\Users\V. Sai Sankeerth\AI_VE\ai-video-studio.bundle" multi-agent-video-editor
cd multi-agent-video-editor
git remote set-url origin https://github.com/SaiSankeerth-dev/multi-agent-video-editor.git
# (create the empty repo on GitHub first, as in Route A step 2)
git push -u origin main
```

---

## Route C — GitHub Desktop (clicks, no commands)

1. Extract `ai-video-studio.zip` to a non-OneDrive folder.
2. GitHub Desktop → **File → Add local repository…** → select the extracted `ai-video-studio` folder.
3. **Publish repository** → Name: `multi-agent-video-editor` → tick/untick *Keep this code private*
   as you prefer → **Publish repository**.

---

### Notes
- The commit is authored as `SaiSankeerth-dev <sankeerthvss@gmail.com>`.
- A broken/locked `.git` exists in `AI_VE\ai-video-studio\` from the failed in-place attempt —
  ignore it; use the zip/bundle instead. You can delete that folder from File Explorer if you like.
- Example MP4s (~7 MB total) are committed under `examples/`. If you'd rather keep the repo
  lean, delete them before pushing and add `examples/*.mp4` to `.gitignore`.
