// Sends the Fudi People knowledge base to the Ask Kofi search index.
// Re-run whenever knowledge-base/ changes (each file's old chunks are replaced).
//
//   INDEX_WEBHOOK_SECRET=... node scripts/index-knowledge-base.mjs [--dry]
//
// Skips: README, 00_INDEX, the superseded/ folder, and non-markdown files (the .xlsx).
import { readdir, readFile } from "node:fs/promises";
import { join, relative, sep } from "node:path";

const KB = new URL("../../spicesOftheWorld/knowledge-base/", import.meta.url);
const ENDPOINT = "https://joiulbstppifvozycivv.supabase.co/functions/v1/index-knowledge";
const secret = process.env.INDEX_WEBHOOK_SECRET;
const dry = process.argv.includes("--dry");
// --only=regional/,fennel   index just files whose path contains one of these (comma-separated)
const onlyArgs = (process.argv.find((a) => a.startsWith("--only="))?.slice(7) ?? "").split(",").filter(Boolean);
if (!secret && !dry) {
  console.error("Set INDEX_WEBHOOK_SECRET first.");
  process.exit(1);
}

async function* walk(dir) {
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) {
      if (e.name === "superseded") continue;
      yield* walk(p);
    } else if (e.name.endsWith(".md") && e.name !== "README.md" && !e.name.startsWith("00_")) {
      yield p;
    }
  }
}

const root = KB.pathname.replace(/^\/([A-Za-z]:)/, "$1");
const files = [];
for await (const f of walk(decodeURIComponent(root))) files.push(f);
files.sort();

// The edge function has a small CPU budget per request, so big files go up in parts of ~MAX_PART
// characters, split at "## " headings. Every part repeats the file's "# Title" line for context.
const MAX_PART = 3500;
function parts(markdown) {
  if (markdown.length <= MAX_PART) return [markdown];
  const text = markdown.replace(/\r\n?/g, "\n");
  const h1 = /^#\s+.+$/m.exec(text)?.[0] ?? "";
  const [intro, ...rawSecs] = text.split(/^(?=##\s)/m);
  // A single section bigger than MAX_PART is cut at paragraph breaks, repeating its "## " heading.
  const secs = rawSecs.flatMap((sec) => {
    if (sec.length <= MAX_PART) return [sec];
    const head = sec.split("\n")[0];
    const pieces = [];
    let acc = "";
    for (const para of sec.split(/\n\n+/)) {
      if (acc && acc.length + para.length > MAX_PART) {
        pieces.push(acc + "\n\n");
        acc = head + " (cont.)\n\n";
      }
      acc += (acc && !acc.endsWith("\n\n") ? "\n\n" : "") + para;
    }
    if (acc.trim()) pieces.push(acc + "\n\n");
    return pieces;
  });
  const out = [];
  let cur = intro;
  for (const s of secs) {
    if (cur.length + s.length > MAX_PART && cur.trim() && cur.trim() !== h1) {
      out.push(cur);
      cur = h1 + "\n\n";
    }
    cur += s;
  }
  if (cur.trim()) out.push(cur);
  return out;
}

let total = 0;
for (const f of files) {
  const base = relative(decodeURIComponent(root), f).split(sep).join("/");
  const markdown = await readFile(f, "utf8");
  if (onlyArgs.length && !onlyArgs.some((s) => base.includes(s))) continue;
  const pieces = parts(markdown);
  if (dry) {
    console.log(`would index ${base} (${markdown.length} chars, ${pieces.length} part${pieces.length > 1 ? "s" : ""})`);
    continue;
  }
  for (const [n, piece] of pieces.entries()) {
    const source = pieces.length > 1 ? `${base}#part${n + 1}` : base;
    // The function occasionally hits a worker resource limit (546); a retry normally succeeds.
    let res, body;
    for (let attempt = 1; attempt <= 4; attempt++) {
      res = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", "x-index-secret": secret },
        body: JSON.stringify({ source, markdown: piece }),
      });
      body = await res.json().catch(() => ({}));
      if (res.ok || attempt === 4) break;
      await new Promise((r) => setTimeout(r, 2000 * attempt));
    }
    if (!res.ok) {
      console.error(`FAILED ${source}: ${res.status} ${body.error ?? ""}`);
      process.exitCode = 1;
      continue;
    }
    total += body.chunks;
    console.log(`${source}: ${body.chunks} chunks`);
  }
}
console.log(dry ? `${files.length} files` : `Done: ${files.length} files, ${total} chunks`);
