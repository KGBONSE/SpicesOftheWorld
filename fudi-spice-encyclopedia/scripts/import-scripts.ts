/**
 * One-off import: creates a DRAFT article for each .md/.txt file in a folder.
 *   npm run import:scripts                          # reads ./content/scripts
 *   npm run import:scripts -- --dir ../spicesOftheWorld/scripts
 *   npm run import:scripts -- --dry-run             # show what would happen, change nothing
 *   npm run import:scripts -- --include-all         # also import *-filming-script / *-read-aloud files
 *
 * - Title and slug come from the filename. Content is stored exactly as written (never rewritten).
 * - Articles are created as drafts (published = false).
 * - Existing slugs are skipped, so re-running never overwrites edits you made in the admin.
 * Needs SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env.local (server-side only).
 */
import { readdirSync, readFileSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { config } from 'dotenv'
import { createClient } from '@supabase/supabase-js'
import { cleanText, isProductionVariant, slugFromFilename, titleFromFilename } from './importLib'

config({ path: '.env.local' })
config()

const args = process.argv.slice(2)
const flag = (name: string) => args.includes(name)
const dirIdx = args.indexOf('--dir')
const dir = resolve(dirIdx >= 0 ? args[dirIdx + 1] : 'content/scripts')
const dryRun = flag('--dry-run')
const includeAll = flag('--include-all')

const files = readdirSync(dir)
  .filter((f) => /\.(md|txt)$/i.test(f) && f.toLowerCase() !== 'readme.md')
  .filter((f) => includeAll || !isProductionVariant(f))
  .sort()

if (files.length === 0) {
  console.error(`No .md/.txt files found in ${dir}`)
  process.exit(1)
}

const url = process.env.SUPABASE_URL
const key = process.env.SUPABASE_SERVICE_ROLE_KEY
if (!dryRun && (!url || !key)) {
  console.error('Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env.local')
  process.exit(1)
}
const db = dryRun ? null : createClient(url!, key!, { auth: { persistSession: false } })

const seen = new Set<string>()
let created = 0
let skipped = 0
let failed = 0

for (const file of files) {
  const slug = slugFromFilename(file)
  const title = titleFromFilename(file)
  if (seen.has(slug)) {
    console.warn(`SKIP  ${file}: duplicate slug "${slug}" in this batch`)
    skipped++
    continue
  }
  seen.add(slug)

  if (!db) {
    console.log(`WOULD CREATE  ${slug}  ("${title}")`)
    created++
    continue
  }

  const existing = await db.from('articles').select('id').eq('slug', slug).maybeSingle()
  if (existing.data) {
    console.log(`SKIP  ${slug}: already exists`)
    skipped++
    continue
  }

  const body = cleanText(readFileSync(join(dir, file), 'utf8'))
  const ins = await db.from('articles').insert({ slug, title, published: false }).select('id').single()
  if (ins.error) {
    console.error(`FAIL  ${slug}: ${ins.error.message}`)
    failed++
    continue
  }
  const bodyRes = await db.from('article_bodies').insert({ article_id: ins.data.id, body_md: body })
  if (bodyRes.error) {
    // Don't leave a bodiless article behind.
    await db.from('articles').delete().eq('id', ins.data.id)
    console.error(`FAIL  ${slug}: ${bodyRes.error.message}`)
    failed++
    continue
  }
  console.log(`OK    ${slug}`)
  created++
}

console.log(`\n${dryRun ? 'Dry run: ' : ''}${created} ${dryRun ? 'would be created' : 'created'}, ${skipped} skipped, ${failed} failed (${files.length} files)`)
if (failed) process.exit(1)
