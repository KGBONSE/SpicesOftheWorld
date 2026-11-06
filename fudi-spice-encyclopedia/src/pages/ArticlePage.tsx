import { Link, useParams } from 'react-router-dom'
import Seo from '../components/Seo'
import Markdown from '../components/Markdown'
import Paywall from '../components/Paywall'
import BuyBar from '../components/BuyBar'
import { ErrorMessage, Loading } from '../components/StateMessage'
import { useAuth } from '../context/AuthContext'
import { useAsync } from '../hooks/useAsync'
import { fetchArticle, fetchProduct, fetchRegions } from '../lib/api'
import NotFound from './NotFound'

export default function ArticlePage() {
  const { slug = '' } = useParams()
  const { isMember, loading: authLoading, session } = useAuth()
  // Re-fetch when auth settles: the server decides how much text we get back.
  const article = useAsync(() => (authLoading ? Promise.resolve(undefined) : fetchArticle(slug, isMember)), [slug, isMember, authLoading, session?.user.id])
  const productId = article.data?.product_id ?? null
  const product = useAsync(() => fetchProduct(productId), [productId])
  const regions = useAsync(fetchRegions, [])

  if (article.loading || authLoading) return <Loading />
  if (article.error) return <ErrorMessage message={article.error} />
  const a = article.data
  if (!a) return <NotFound />

  const region = regions.data?.find((r) => r.slug === a.region_slug)

  return (
    <article className="pb-28 md:pb-16">
      <Seo title={a.title} description={a.summary} image={a.cover_image_url} path={`/encyclopedia/${a.slug}`} type="article" />

      <header className="container-page max-w-3xl pt-10 text-center">
        <nav aria-label="Breadcrumb" className="text-sm text-ink/70">
          <Link to="/encyclopedia" className="hover:underline">Encyclopedia</Link>
          {region && (
            <>
              {' / '}
              <Link to={`/encyclopedia?region=${region.slug}`} className="hover:underline">{region.name}</Link>
            </>
          )}
        </nav>
        <h1 className="mt-4 text-4xl font-extrabold leading-tight text-maroon sm:text-5xl">{a.title}</h1>
        {a.summary && <p className="mt-4 text-lg text-ink/80">{a.summary}</p>}
      </header>

      {a.cover_image_url && (
        <div className="container-page mt-8 max-w-4xl">
          <img src={a.cover_image_url} alt={`${a.title}`} className="aspect-[16/9] w-full rounded-2xl object-cover" />
        </div>
      )}

      <div className="container-page mt-10">
        <Markdown>{a.body_md}</Markdown>
        {a.is_preview && <Paywall />}
      </div>

      {product.data && <BuyBar product={product.data} />}
    </article>
  )
}
