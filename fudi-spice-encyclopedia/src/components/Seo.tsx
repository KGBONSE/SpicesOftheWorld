import { Helmet } from 'react-helmet-async'
import { SITE_URL } from '../lib/supabase'

interface Props {
  title?: string
  description?: string
  image?: string | null
  path?: string
  type?: 'website' | 'article'
}

const SITE = 'Fudi People Spice Encyclopedia'

export default function Seo({ title, description, image, path, type = 'website' }: Props) {
  const fullTitle = title ? `${title} | ${SITE}` : SITE
  const desc = description?.slice(0, 160)
  const url = path ? `${SITE_URL}${path}` : undefined
  return (
    <Helmet>
      <title>{fullTitle}</title>
      {desc && <meta name="description" content={desc} />}
      <meta property="og:site_name" content={SITE} />
      <meta property="og:type" content={type} />
      <meta property="og:title" content={fullTitle} />
      {desc && <meta property="og:description" content={desc} />}
      {image && <meta property="og:image" content={image} />}
      {url && <meta property="og:url" content={url} />}
      {url && <link rel="canonical" href={url} />}
      <meta name="twitter:card" content={image ? 'summary_large_image' : 'summary'} />
    </Helmet>
  )
}
