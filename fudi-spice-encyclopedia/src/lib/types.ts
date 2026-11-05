export interface Region {
  slug: string
  name: string
  sort_order: number
}

export interface Product {
  id: string
  name: string
  region_slug: string | null
  description: string
  price_display: string
  image_url: string | null
  buy_url: string
}

/** Public article metadata (no body). */
export interface ArticleSummary {
  id: string
  slug: string
  title: string
  region_slug: string | null
  summary: string
  cover_image_url: string | null
  featured: boolean
  published: boolean
  published_at: string | null
}

/** Admin view of an article, including editable fields. */
export interface ArticleAdmin extends ArticleSummary {
  preview_percent: number
  product_id: string | null
  body_md: string
}

/** Result of the get_article() paywall function. */
export interface ArticleView {
  id: string
  slug: string
  title: string
  region_slug: string | null
  summary: string
  cover_image_url: string | null
  product_id: string | null
  published_at: string | null
  updated_at: string
  body_md: string
  is_preview: boolean
}

export interface Profile {
  id: string
  email: string | null
  role: 'user' | 'admin'
  membership_status: 'free' | 'member'
  current_period_end: string | null
}
