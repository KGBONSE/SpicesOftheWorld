import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ErrorMessage, Loading } from '../../components/StateMessage'
import { useAsync } from '../../hooks/useAsync'
import { adminDeleteArticle, adminListArticles } from '../../lib/api'

export default function AdminArticles() {
  const [version, setVersion] = useState(0)
  const [filter, setFilter] = useState<'all' | 'draft' | 'published'>('all')
  const list = useAsync(adminListArticles, [version])

  if (list.loading) return <Loading />
  if (list.error) return <ErrorMessage message={list.error} />

  const rows = (list.data ?? []).filter((a) => filter === 'all' || (filter === 'published') === a.published)
  const drafts = (list.data ?? []).filter((a) => !a.published).length

  async function remove(id: string, title: string) {
    if (!window.confirm(`Delete "${title}"? This cannot be undone.`)) return
    await adminDeleteArticle(id)
    setVersion((v) => v + 1)
  }

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="text-sm text-ink/70">{list.data?.length ?? 0} articles · {drafts} drafts</p>
        <div className="flex items-center gap-3">
          <label htmlFor="filter" className="sr-only">Filter</label>
          <select id="filter" className="field w-auto" value={filter} onChange={(e) => setFilter(e.target.value as typeof filter)}>
            <option value="all">All</option>
            <option value="draft">Drafts</option>
            <option value="published">Published</option>
          </select>
          <Link to="/admin/articles/new" className="btn-primary">New article</Link>
        </div>
      </div>

      <ul className="mt-6 divide-y divide-ink/10 rounded-xl bg-white ring-1 ring-ink/10">
        {rows.map((a) => (
          <li key={a.id} className="flex items-center justify-between gap-3 p-4">
            <div className="min-w-0">
              <Link to={`/admin/articles/${a.id}`} className="block truncate font-bold hover:underline">{a.title}</Link>
              <p className="text-xs text-ink/70">/{a.slug} · {a.published ? 'Published' : 'Draft'}</p>
            </div>
            <button className="text-sm font-semibold text-maroon underline" onClick={() => remove(a.id, a.title)}>Delete</button>
          </li>
        ))}
        {rows.length === 0 && <li className="p-6 text-center text-ink/70">Nothing here yet.</li>}
      </ul>
    </div>
  )
}
