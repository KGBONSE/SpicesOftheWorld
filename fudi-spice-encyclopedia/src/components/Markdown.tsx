import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeSanitize from 'rehype-sanitize'

/** Renders Markdown with raw HTML disabled (react-markdown default) and output sanitised. */
export default function Markdown({ children }: { children: string }) {
  return (
    <div className="prose prose-lg mx-auto max-w-[68ch] prose-headings:font-extrabold prose-headings:text-maroon prose-a:text-maroon prose-blockquote:border-marigold prose-img:rounded-xl">
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>
        {children}
      </ReactMarkdown>
    </div>
  )
}
