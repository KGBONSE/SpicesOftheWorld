import type { Product } from '../lib/types'

/** Sticky bottom bar on mobile; floating card on desktop. Links to the live shop. */
export default function BuyBar({ product }: { product: Product }) {
  return (
    <aside
      aria-label="Buy this blend"
      className="fixed inset-x-0 bottom-0 z-40 border-t border-ink/10 bg-cream/95 px-4 py-3 backdrop-blur md:inset-x-auto md:bottom-6 md:right-6 md:w-80 md:rounded-2xl md:border md:shadow-lg"
    >
      <div className="flex items-center justify-between gap-3">
        <div className="min-w-0">
          <p className="truncate text-sm font-extrabold">{product.name}</p>
          {product.price_display && <p className="text-xs text-ink/70">{product.price_display}</p>}
        </div>
        <a href={product.buy_url} target="_blank" rel="noopener" className="btn-primary shrink-0">
          Buy the blend
        </a>
      </div>
    </aside>
  )
}
