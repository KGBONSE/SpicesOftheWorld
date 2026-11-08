// Publishes or updates articles straight from content/drafts/*.md (no copy-pasting).
//
//   INDEX_WEBHOOK_SECRET=... node scripts/publish-drafts.mjs <slug> [<slug> ...] [--order=130]
//
// Each draft has front matter (slug, title, region, sub_region, summary, reading_minutes,
// preview_percent, product) then the article body; everything from "## NOTES FOR KOFI" on is dropped.
// After publishing, each article is indexed for Ask Kofi one at a time (the database trigger can miss
// some when many are published together), and the chunk count is printed.
import { readFile } from "node:fs/promises";

const BASE = "https://joiulbstppifvozycivv.supabase.co/functions/v1";
const secret = process.env.INDEX_WEBHOOK_SECRET;
if (!secret) {
  console.error("Set INDEX_WEBHOOK_SECRET first.");
  process.exit(1);
}
const args = process.argv.slice(2);
const slugs = args.filter((a) => !a.startsWith("--"));
let order = Number(args.find((a) => a.startsWith("--order="))?.slice(8) ?? 0);

async function load(slug) {
  const raw = (await readFile(new URL(`../content/drafts/${slug}.md`, import.meta.url), "utf8")).replace(/\r\n/g, "\n");
  const m = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/.exec(raw);
  if (!m) throw new Error(`${slug}: no front matter`);
  const meta = {};
  for (const line of m[1].split("\n")) {
    const i = line.indexOf(":");
    meta[line.slice(0, i).trim()] = line.slice(i + 1).trim().replace(/^"|"$/g, "");
  }
  const body = m[2].split(/\n---\n\n## NOTES FOR KOFI/)[0].trim();
  return {
    slug: meta.slug,
    title: meta.title,
    region: meta.region,
    sub_region: meta.sub_region,
    summary: meta.summary,
    reading_minutes: Number(meta.reading_minutes),
    preview_percent: Number(meta.preview_percent),
    product: meta.product || null,
    sort_order: order ? order++ : Number(meta.sort_order ?? 0),
    body,
  };
}

const post = async (path, payload) => {
  const res = await fetch(`${BASE}/${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-index-secret": secret },
    body: JSON.stringify(payload),
  });
  return { ok: res.ok, status: res.status, body: await res.json().catch(() => ({})) };
};

const articles = [];
for (const s of slugs) articles.push(await load(s));

// publish in small groups
for (let i = 0; i < articles.length; i += 4) {
  const group = articles.slice(i, i + 4);
  const r = await post("publish-content", { articles: group });
  if (!r.ok) {
    console.error("publish-content failed:", r.status, r.body);
    process.exit(1);
  }
  for (const x of r.body.results) console.log(`${x.slug}: ${x.status}`);
}

// index one at a time, retrying, so Ask Kofi always has the new text
for (const a of articles) {
  let chunks = 0;
  for (let attempt = 1; attempt <= 4 && !chunks; attempt++) {
    const r = await post("index-article", { slug: a.slug });
    chunks = r.body?.results?.[0]?.chunks ?? 0;
    if (!chunks) await new Promise((res) => setTimeout(res, 2000 * attempt));
  }
  console.log(`${a.slug}: indexed ${chunks} chunks${chunks ? "" : "  <-- CHECK"}`);
}
