import { supabase } from './supabase'
import type { ArticleAdmin, ArticleSummary, ArticleView, Product, Region } from './types'
import { demoArticles, demoArticleView, demoProducts, demoRegions } from './demoData'

const SUMMARY_COLS = 'id,slug,title,region_slug,summary,cover_image_url,featured,published,published_at'

function check<T>(res: { data: T | null; error: { message: string } | null }): T {
  if (res.error) throw new Error(res.error.message)
  return res.data as T
}

export async function fetchRegions(): Promise<Region[]> {
  if (!supabase) return demoRegions
  return check(await supabase.from('regions').select('*').order('sort_order'))
}

export async function fetchArticles(): Promise<ArticleSummary[]> {
  if (!supabase) return demoArticles
  return check(
    await supabase.from('articles').select(SUMMARY_COLS).eq('published', true).order('title'),
  )
}

export async function fetchFeatured(): Promise<ArticleSummary[]> {
  if (!supabase) return demoArticles.filter((a) => a.featured)
  return check(
    await supabase
      .from('articles')
      .select(SUMMARY_COLS)
      .eq('published', true)
      .eq('featured', true)
      .order('published_at', { ascending: false })
      .limit(6),
  )
}

/** Paywall-enforced: the database decides how much text comes back. */
export async function fetchArticle(slug: string, isMember: boolean): Promise<ArticleView | null> {
  if (!supabase) return demoArticleView(slug, isMember)
  const rows = check(await supabase.rpc('get_article', { p_slug: slug })) as ArticleView[]
  return rows[0] ?? null
}

export async function fetchProduct(id: string | null): Promise<Product | null> {
  if (!id) return null
  if (!supabase) return demoProducts.find((p) => p.id === id) ?? null
  return check(await supabase.from('products').select('*').eq('id', id).maybeSingle())
}

export async function fetchProducts(): Promise<Product[]> {
  if (!supabase) return demoProducts
  return check(await supabase.from('products').select('*').order('name'))
}

// ---------- admin ----------
function requireDb() {
  if (!supabase) throw new Error('Supabase is not configured. Add your keys to .env.local.')
  return supabase
}

export async function adminListArticles(): Promise<ArticleSummary[]> {
  return check(await requireDb().from('articles').select(SUMMARY_COLS).order('title'))
}

export async function adminGetArticle(id: string): Promise<ArticleAdmin | null> {
  const db = requireDb()
  const a = check(await db.from('articles').select('*').eq('id', id).maybeSingle()) as Omit<ArticleAdmin, 'body_md'> | null
  if (!a) return null
  const b = check(await db.from('article_bodies').select('body_md').eq('article_id', id).maybeSingle()) as { body_md: string } | null
  return { ...a, body_md: b?.body_md ?? '' }
}

export async function adminSaveArticle(a: Partial<ArticleAdmin> & { title: string; slug: string }): Promise<string> {
  const db = requireDb()
  const { body_md, id, ...meta } = a
  let articleId = id
  if (articleId) {
    check(await db.from('articles').update(meta).eq('id', articleId).select('id').single())
  } else {
    articleId = (check(await db.from('articles').insert(meta).select('id').single()) as { id: string }).id
  }
  check(await db.from('article_bodies').upsert({ article_id: articleId, body_md: body_md ?? '' }).select('article_id'))
  return articleId!
}

export async function adminDeleteArticle(id: string) {
  check(await requireDb().from('articles').delete().eq('id', id).select('id'))
}

export async function adminSaveProduct(p: Partial<Product> & { name: string; buy_url: string }): Promise<void> {
  const db = requireDb()
  const { id, ...rest } = p
  if (id) check(await db.from('products').update(rest).eq('id', id).select('id'))
  else check(await db.from('products').insert(rest).select('id'))
}

export async function adminDeleteProduct(id: string) {
  check(await requireDb().from('products').delete().eq('id', id).select('id'))
}

export async function uploadCover(file: File): Promise<string> {
  const db = requireDb()
  const ext = file.name.split('.').pop()?.toLowerCase().replace(/[^a-z0-9]/g, '') || 'jpg'
  const path = `${crypto.randomUUID()}.${ext}`
  const { error } = await db.storage.from('covers').upload(path, file, { contentType: file.type })
  if (error) throw new Error(error.message)
  return db.storage.from('covers').getPublicUrl(path).data.publicUrl
}

// ---------- memberships ----------
export async function startCheckout(plan: 'monthly' | 'annual'): Promise<string> {
  const db = requireDb()
  const { data, error } = await db.functions.invoke('create-checkout', { body: { plan } })
  if (error) throw new Error(error.message)
  return (data as { url: string }).url
}

export async function openCustomerPortal(): Promise<string> {
  const db = requireDb()
  const { data, error } = await db.functions.invoke('customer-portal')
  if (error) throw new Error(error.message)
  return (data as { url: string }).url
}

export function slugify(s: string): string {
  return s
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}
