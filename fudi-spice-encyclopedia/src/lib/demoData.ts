// PLACEHOLDER data used only when Supabase isn't configured yet, so the UI can be previewed.
// It is not real content. Replace by connecting Supabase and importing your scripts.
import type { ArticleSummary, ArticleView, Product, Region } from './types'

export const demoRegions: Region[] = [
  { slug: 'africa', name: 'Africa', sort_order: 1 },
  { slug: 'middle-east', name: 'Middle East', sort_order: 2 },
  { slug: 'south-asia', name: 'South Asia', sort_order: 3 },
  { slug: 'east-asia', name: 'East Asia', sort_order: 4 },
  { slug: 'southeast-asia', name: 'Southeast Asia', sort_order: 5 },
  { slug: 'americas', name: 'Americas', sort_order: 6 },
  { slug: 'europe', name: 'Europe', sort_order: 7 },
]

export const demoProducts: Product[] = [
  { id: 'p1', name: 'Yaji (Suya Spice)', region_slug: 'africa', description: 'Placeholder.', price_display: '£0.00', image_url: null, buy_url: 'https://fudipeople.com' },
  { id: 'p2', name: 'Garam Masala', region_slug: 'south-asia', description: 'Placeholder.', price_display: '£0.00', image_url: null, buy_url: 'https://fudipeople.com' },
]

const base = { cover_image_url: null, featured: true, published: true, published_at: '2026-01-01T00:00:00Z' }

export const demoArticles: ArticleSummary[] = [
  { ...base, id: 'a1', slug: 'demo-yaji', title: 'Demo: Yaji', region_slug: 'africa', summary: 'Placeholder article to preview the layout and paywall.' },
  { ...base, id: 'a2', slug: 'demo-garam-masala', title: 'Demo: Garam Masala', region_slug: 'south-asia', summary: 'Placeholder article to preview the index.' },
]

const demoBody = [
  '## Placeholder',
  'This first paragraph is the free preview. Real article text will appear here once your scripts are imported.',
  'Second paragraph of placeholder text.',
  'Third paragraph of placeholder text.',
  'Fourth paragraph: members only.',
].join('\n\n')

/** Mimics the server-side get_article() preview rule for demo mode only. */
export function demoArticleView(slug: string, isMember: boolean): ArticleView | null {
  const a = demoArticles.find((x) => x.slug === slug)
  if (!a) return null
  const paras = demoBody.split(/\n{2,}/)
  return {
    ...a,
    product_id: a.region_slug === 'africa' ? 'p1' : 'p2',
    updated_at: a.published_at!,
    body_md: isMember ? demoBody : paras.slice(0, 2).join('\n\n'),
    is_preview: !isMember,
  }
}
