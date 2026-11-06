import { Link } from 'react-router-dom'
import Seo from '../components/Seo'
import ArticleCard from '../components/ArticleCard'
import { ErrorMessage } from '../components/StateMessage'
import { useAsync } from '../hooks/useAsync'
import { fetchFeatured, fetchRegions } from '../lib/api'

export default function Home() {
  const featured = useAsync(fetchFeatured, [])
  const regions = useAsync(fetchRegions, [])
  const regionName = (slug: string | null) => regions.data?.find((r) => r.slug === slug)?.name

  return (
    <>
      <Seo description="Where the world's spices really come from, traced by a farmer-founder. From Makola Market in Accra to our farm in Sidcup." path="/" />

      {/* Hero: DRAFT COPY, edit in your own words */}
      <section className="bg-maroon text-cream">
        <div className="container-page py-16 sm:py-24">
          <p className="text-sm font-bold uppercase tracking-widest text-gold">Fudi People Spice Encyclopedia</p>
          <h1 className="mt-4 max-w-3xl text-4xl font-extrabold leading-tight sm:text-6xl">
            Where your spices really come from.
          </h1>
          <p className="mt-6 max-w-2xl text-lg text-cream/90">
            I'm Kofi. I grew up around Makola Market in Accra, and today I grow chillies and okra on my farm in
            Sidcup. This is the story of the world's spices, told by someone who handles them from farm to jar.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link to="/encyclopedia" className="btn-primary">Explore the encyclopedia</Link>
            <Link to="/about" className="btn border-2 border-cream/40 hover:border-cream">Read my story</Link>
          </div>
        </div>
      </section>

      <section className="container-page py-14" aria-labelledby="featured-h">
        <h2 id="featured-h" className="text-3xl font-extrabold">Featured spices</h2>
        {featured.error && <ErrorMessage message={featured.error} />}
        {featured.data && featured.data.length === 0 && (
          <p className="mt-4 text-ink/70">Articles are on their way. Check back soon.</p>
        )}
        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {featured.data?.map((a) => (
            <ArticleCard key={a.id} article={a} regionName={regionName(a.region_slug)} />
          ))}
        </div>
      </section>

      <section className="bg-cream-dark py-14" aria-labelledby="regions-h">
        <div className="container-page">
          <h2 id="regions-h" className="text-3xl font-extrabold">Browse by region</h2>
          <ul className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
            {regions.data?.map((r) => (
              <li key={r.slug}>
                <Link
                  to={`/encyclopedia?region=${r.slug}`}
                  className="flex min-h-20 items-center justify-center rounded-xl bg-white p-4 text-center font-extrabold ring-1 ring-ink/10 hover:bg-maroon hover:text-cream"
                >
                  {r.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section className="container-page py-16">
        <div className="rounded-3xl bg-ink p-8 text-center text-cream sm:p-14">
          <h2 className="text-3xl font-extrabold">Read every story in full</h2>
          <p className="mx-auto mt-3 max-w-xl text-cream/85">
            Every article opens with a free preview. Become a member to unlock the full history of every spice.
          </p>
          <Link to="/membership" className="btn-primary mt-7">Become a member</Link>
        </div>
      </section>
    </>
  )
}
