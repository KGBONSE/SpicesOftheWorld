import { Link } from 'react-router-dom'
import type { ArticleSummary } from '../lib/types'

export default function ArticleCard({ article, regionName }: { article: ArticleSummary; regionName?: string }) {
  return (
    <article className="group overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-ink/10 transition hover:shadow-md">
      <Link to={`/encyclopedia/${article.slug}`} className="block">
        {article.cover_image_url ? (
          <img
            src={article.cover_image_url}
            alt=""
            loading="lazy"
            className="aspect-[4/3] w-full object-cover"
          />
        ) : (
          <div
            className="flex aspect-[4/3] w-full items-center justify-center bg-maroon text-4xl font-extrabold text-gold"
            aria-hidden="true"
          >
            {article.title.charAt(0)}
          </div>
        )}
        <div className="p-5">
          {regionName && (
            <p className="text-xs font-bold uppercase tracking-wider text-marigold-dark">{regionName}</p>
          )}
          <h3 className="mt-1 text-xl font-extrabold leading-snug group-hover:text-maroon">{article.title}</h3>
          {article.summary && <p className="mt-2 line-clamp-3 text-sm text-ink/80">{article.summary}</p>}
        </div>
      </Link>
    </article>
  )
}
