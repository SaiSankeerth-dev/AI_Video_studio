import { chromium } from "playwright"; // or use puppeteer bundled with hyperframes
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

// We can render the character sheet views using hyperframes snapshot
// by setting camera and lighting states in a dedicated composition or via scene3d
console.log("Renderer ready.");
