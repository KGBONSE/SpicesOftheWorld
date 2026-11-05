import { useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import Seo from '../components/Seo'
import ArticleCard from '../components/ArticleCard'
import { ErrorMessage, Loading } from '../components/StateMessage'
import { useAsync } from '../hooks/useAsync'
import { fetchArticles, fetchRegions } from '../lib/api'

export default function Encyclopedia() {
  const [params, setParams] = useSearchParams()
  const region = params.get('region') ?? ''
  const q = params.get('q') ?? ''
  const articles = useAsync(fetchArticles, [])
  const regions = useAsync(fetchRegions, [])

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase()
    return (articles.data ?? []).filter(
      (a) =>
        (!region || a.region_slug === region) &&
        (!needle || a.title.toLowerCase().includes(needle) || a.summary.toLowerCase().includes(needle)),
    )
  }, [articles.data, region, q])

  const update = (key: string, value: string) => {
    const next = new URLSearchParams(params)
    if (value) next.set(key, value)
    else next.delete(key)
    setParams(next, { replace: true })
  }

  const regionName = (slug: string | null) => regions.data?.find((r) => r.slug === slug)?.name

  return (
    <div className="container-page py-12">
      <Seo title="Encyclopedia" description="Browse the history and origins of the world's spices, by region." path="/encyclopedia" />
      <h1 className="text-4xl font-extrabold">The Encyclopedia</h1>
      <p className="mt-2 max-w-2xl text-ink/80">The history and origins of the world's spices.</p>

      <form role="search" className="mt-8 grid gap-4 sm:grid-cols-[1fr_16rem]" onSubmit={(e) => e.preventDefault()}>
        <div>
          <label htmlFor="q" className="label">Search by name</label>
          <input id="q" type="search" className="field" value={q} placeholder="e.g. cumin" onChange={(e) => update('q', e.target.value)} />
        </div>
        <div>
          <label htmlFor="region" className="label">Region</label>
          <select id="region" className="field" value={region} onChange={(e) => update('region', e.target.value)}>
            <option value="">All regions</option>
            {regions.data?.map((r) => (
              <option key={r.slug} value={r.slug}>{r.name}</option>
            ))}
          </select>
        </div>
      </form>

      {articles.loading && <Loading />}
      {articles.error && <ErrorMessage message={articles.error} />}
      {articles.data && (
        <>
          <p className="mt-6 text-sm text-ink/70" aria-live="polite">
            {filtered.length} {filtered.length === 1 ? 'article' : 'articles'}
          </p>
          <div className="mt-4 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((a) => (
              <ArticleCard key={a.id} article={a} regionName={regionName(a.region_slug)} />
            ))}
          </div>
          {filtered.length === 0 && <p className="mt-8">No spices match that search.</p>}
        </>
      )}
    </div>
  )
}
