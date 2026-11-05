import { useState, type FormEvent } from 'react'
import { ErrorMessage, Loading } from '../../components/StateMessage'
import { useAsync } from '../../hooks/useAsync'
import { adminDeleteProduct, adminSaveProduct, fetchProducts, fetchRegions, uploadCover } from '../../lib/api'
import type { Product } from '../../lib/types'

const EMPTY = { name: '', region_slug: null, description: '', price_display: '', image_url: null, buy_url: '' } as Omit<Product, 'id'> & { id?: string }

export default function AdminProducts() {
  const [version, setVersion] = useState(0)
  const products = useAsync(fetchProducts, [version])
  const regions = useAsync(fetchRegions, [])
  const [form, setForm] = useState<typeof EMPTY | null>(null)
  const [error, setError] = useState<string | null>(null)

  const set = <K extends keyof typeof EMPTY>(k: K, v: (typeof EMPTY)[K]) => setForm((f) => (f ? { ...f, [k]: v } : f))

  async function save(e: FormEvent) {
    e.preventDefault()
    if (!form) return
    setError(null)
    try {
      await adminSaveProduct(form)
      setForm(null)
      setVersion((v) => v + 1)
    } catch (err) {
      setError((err as Error).message)
    }
  }

  async function remove(p: Product) {
    if (!window.confirm(`Delete "${p.name}"? Articles linked to it will lose their Buy button.`)) return
    await adminDeleteProduct(p.id)
    setVersion((v) => v + 1)
  }

  if (products.loading) return <Loading />
  if (products.error) return <ErrorMessage message={products.error} />

  return (
    <div>
      {!form && <button className="btn-primary" onClick={() => setForm({ ...EMPTY })}>New product</button>}

      {form && (
        <form onSubmit={save} className="space-y-4 rounded-xl bg-white p-6 ring-1 ring-ink/10">
          <h2 className="text-xl font-extrabold">{form.id ? 'Edit product' : 'New product'}</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            <div><label htmlFor="pname" className="label">Name</label><input id="pname" required className="field" value={form.name} onChange={(e) => set('name', e.target.value)} /></div>
            <div>
              <label htmlFor="pregion" className="label">Region</label>
              <select id="pregion" className="field" value={form.region_slug ?? ''} onChange={(e) => set('region_slug', e.target.value || null)}>
                <option value="">None</option>
                {regions.data?.map((r) => <option key={r.slug} value={r.slug}>{r.name}</option>)}
              </select>
            </div>
            <div><label htmlFor="pprice" className="label">Price (display text, e.g. £6.50)</label><input id="pprice" className="field" value={form.price_display} onChange={(e) => set('price_display', e.target.value)} /></div>
            <div><label htmlFor="purl" className="label">Buy URL (your shop page)</label><input id="purl" type="url" required className="field" value={form.buy_url} onChange={(e) => set('buy_url', e.target.value)} /></div>
          </div>
          <div><label htmlFor="pdesc" className="label">Description</label><textarea id="pdesc" rows={3} className="field" value={form.description} onChange={(e) => set('description', e.target.value)} /></div>
          <div>
            <label htmlFor="pimg" className="label">Image</label>
            <input id="pimg" type="file" accept="image/*" className="field"
              onChange={async (e) => {
                const f = e.target.files?.[0]
                if (f) try { set('image_url', await uploadCover(f)) } catch (err) { setError((err as Error).message) }
              }} />
            {form.image_url && <img src={form.image_url} alt="Product preview" className="mt-2 h-24 rounded-lg object-cover" />}
          </div>
          <div className="flex gap-3">
            <button type="submit" className="btn-dark">Save</button>
            <button type="button" className="btn-outline" onClick={() => setForm(null)}>Cancel</button>
          </div>
        </form>
      )}
      {error && <p role="alert" className="mt-4 font-semibold text-maroon">{error}</p>}

      <ul className="mt-6 divide-y divide-ink/10 rounded-xl bg-white ring-1 ring-ink/10">
        {products.data?.map((p) => (
          <li key={p.id} className="flex items-center justify-between gap-3 p-4">
            <div className="min-w-0">
              <p className="truncate font-bold">{p.name}</p>
              <p className="truncate text-xs text-ink/70">{p.price_display} · {p.buy_url}</p>
            </div>
            <div className="flex gap-4 text-sm font-semibold">
              <button className="underline" onClick={() => setForm(p)}>Edit</button>
              <button className="text-maroon underline" onClick={() => remove(p)}>Delete</button>
            </div>
          </li>
        ))}
        {products.data?.length === 0 && <li className="p-6 text-center text-ink/70">No products yet.</li>}
      </ul>
    </div>
  )
}
