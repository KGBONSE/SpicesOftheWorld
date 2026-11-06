export function slugFromFilename(file: string): string {
  const base = file.replace(/\.(md|txt)$/i, '')
  return base
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

/** "episode-09-caribbean-jerk.md" -> "Episode 09 Caribbean Jerk" (filename only; content is never touched). */
export function titleFromFilename(file: string): string {
  return file
    .replace(/\.(md|txt)$/i, '')
    .split(/[-_\s]+/)
    .filter(Boolean)
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ')
}

/** Production-only files that sit beside the main episode scripts. Skipped unless --include-all. */
export function isProductionVariant(file: string): boolean {
  return /(filming-script|read-aloud)/i.test(file)
}

/** Strip a UTF-8 BOM and normalise line endings. The text itself is otherwise unchanged. */
export function cleanText(raw: string): string {
  return raw.replace(/^﻿/, '').replace(/\r\n?/g, '\n')
}
