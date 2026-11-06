import { useEffect, useState, type FormEvent } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { ErrorMessage, Loading } from '../../components/StateMessage'
import Markdown from '../../components/Markdown'
import { useAsync } from '../../hooks/useAsync'
import { adminGetArticle, adminSaveArticle, fetchProducts, fetchRegions, slugify, uploadCover } from '../../lib/api'
import type { ArticleAdmin } from '../../lib/types'

const EMPTY: ArticleAdmin = {
  id: '',
  slug: '',
  title: '',
  region_slug: null,
  summary: '',
  cover_image_url: null,
  featured: false,
  published: false,
  published_at: null,
  preview_percent: 25,
  product_id: null,
  body_md: '',
}

export default function AdminArticleEdit() {
  const { id } = useParams()
  const navigate = useNavigate()
  const loaded = useAsync(() => (id ? adminGetArticle(id) : Promise.resolve(null)), [id])
  const regions = useAsync(fetchRegions, [])
  const products = useAsync(fetchProducts, [])
  const [form, setForm] = useState<ArticleAdmin>(EMPTY)
  const [slugTouched, setSlugTouched] = useState(false)
  const [preview, setPreview] = useState(false)
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState<{ ok: boolean; text: string } | null>(null)

  useEffect(() => {
    if (loaded.data) {
      setForm(loaded.data)
      setSlugTouched(true)
    }
  }, [loaded.data])

  const set = <K extends keyof ArticleAdmin>(k: K, v: ArticleAdmin[K]) => setForm((f) => ({ ...f, [k]: v }))

  async function onCover(file: File | undefined) {
    if (!file) return
    setMsg(null)
    try {
      set('cover_image_url', await uploadCover(file))
    } catch (e) {
      setMsg({ ok: false, text: (e as Error).message })
    }
  }

  async function save(e: FormEvent) {
    e.preventDefault()
    setBusy(true)
    setMsg(null)
    try {
      const { id: formId, published_at: _p, ...rest } = form
      void _p
      const savedId = await adminSaveArticle({ ...rest, ...(formId ? { id: formId } : {}) })
      setMsg({ ok: true, text: 'Saved.' })
      if (!id) navigate(`/admin/articles/${savedId}`, { replace: true })
    } catch (err) {
      setMsg({ ok: false, text: (err as Error).message })
    } finally {
      setBusy(false)
    }
  }

  if (id && loaded.loading) return <Loading />
  if (loaded.error) return <ErrorMessage message={loaded.error} />

  return (
    <form onSubmit={save} className="space-y-5">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-extrabold">{id ? 'Edit article' : 'New article'}</h2>
        <Link to="/admin" className="text-sm underline">Back to list</Link>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <div>
          <label htmlFor="title" className="label">Title</label>
          <input id="title" required className="field" value={form.title}
            onChange={(e) => {
              set('title', e.target.value)
              if (!slugTouched) set('slug', slugify(e.target.value))
            }} />
        </div>
        <div>
          <label htmlFor="slug" className="label">Slug (URL)</label>
          <input id="slug" required pattern="[a-z0-9]+(-[a-z0-9]+)*" title="Lowercase letters, numbers and hyphens" className="field" value={form.slug}
            onChange={(e) => { setSlugTouched(true); set('slug', e.target.value) }} />
        </div>
        <div>
          <label htmlFor="region" className="label">Region</label>
          <select id="region" className="field" value={form.region_slug ?? ''} onChange={(e) => set('region_slug', e.target.value || null)}>
            <option value="">None</option>
            {regions.data?.map((r) => <option key={r.slug} value={r.slug}>{r.name}</option>)}
          </select>
        </div>
        <div>
          <label htmlFor="product" className="label">Linked product ("Buy the blend")</label>
          <select id="product" className="field" value={form.product_id ?? ''} onChange={(e) => set('product_id', e.target.value || null)}>
            <option value="">None</option>
            {products.data?.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
        </div>
      </div>

      <div>
        <label htmlFor="summary" className="label">Summary</label>
        <textarea id="summary" rows={3} className="field" value={form.summary} onChange={(e) => set('summary', e.target.value)} />
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <div>
          <label htmlFor="cover" className="label">Cover image</label>
          <input id="cover" type="file" accept="image/*" className="field" onChange={(e) => onCover(e.target.files?.[0])} />
          {form.cover_image_url && <img src={form.cover_image_url} alt="Cover preview" className="mt-2 h-28 rounded-lg object-cover" />}
        </div>
        <div>
          <label htmlFor="pct" className="label">Free preview: {form.preview_percent}% of the article</label>
          <input id="pct" type="range" min={0} max={100} step={5} className="w-full" value={form.preview_percent}
            onChange={(e) => set('preview_percent', Number(e.target.value))} />
        </div>
      </div>

      <div>
        <div className="flex items-center justify-between">
          <label htmlFor="body" className="label">Body (Markdown)</label>
          <button type="button" className="text-sm underline" onClick={() => setPreview(!preview)}>{preview ? 'Edit' : 'Preview'}</button>
        </div>
        {preview ? (
          <div className="rounded-lg bg-white p-6 ring-1 ring-ink/10"><Markdown>{form.body_md}</Markdown></div>
        ) : (
          <textarea id="body" rows={22} className="field font-mono text-sm" value={form.body_md} onChange={(e) => set('body_md', e.target.value)} />
        )}
      </div>

      <div className="flex flex-wrap gap-6">
        <label className="flex items-center gap-2 font-semibold">
          <input type="checkbox" checked={form.published} onChange={(e) => set('published', e.target.checked)} /> Published
        </label>
        <label className="flex items-center gap-2 font-semibold">
          <input type="checkbox" checked={form.featured} onChange={(e) => set('featured', e.target.checked)} /> Featured on home page
        </label>
      </div>

      <div className="flex items-center gap-4">
        <button type="submit" disabled={busy} className="btn-dark disabled:opacity-60">{busy ? 'Saving…' : 'Save'}</button>
        {form.published && form.slug && <Link to={`/encyclopedia/${form.slug}`} className="text-sm underline">View live</Link>}
        {msg && <p role={msg.ok ? 'status' : 'alert'} className={`font-semibold ${msg.ok ? '' : 'text-maroon'}`}>{msg.text}</p>}
      </div>
    </form>
  )
}
