import { Link } from 'react-router-dom'
import Seo from '../components/Seo'

// DRAFT COPY: built only from facts in the project brief. Kofi to rewrite in his own voice.
export default function About() {
  return (
    <div className="container-page max-w-3xl py-14">
      <Seo title="About Kofi" description="Farmer-founder of Fudi People: from Makola Market in Accra to a spice farm in Sidcup, London." path="/about" />
      <p className="text-sm font-bold uppercase tracking-widest text-marigold-dark">About</p>
      <h1 className="mt-2 text-4xl font-extrabold text-maroon sm:text-5xl">A farmer tracing where spices come from</h1>

      <div className="prose prose-lg mt-8 max-w-none prose-headings:font-extrabold prose-headings:text-maroon">
        <p>
          I'm Kofi, founder of Fudi People, a spice and chilli oil brand based in London. My roots are in Ghana, and
          some of my earliest food memories are of Makola Market in Accra.
        </p>
        <h2>From Makola Market to Sidcup</h2>
        <p>
          Today I grow chillies and okra on my farm in Sidcup. Those farm-grown chillies and carefully sourced dried
          spices go into blends from six regions of the world, and into a chilli oil that is vegan: just spices and
          chillies.
        </p>
        <h2>Why an encyclopedia</h2>
        <p>
          I'm not a detached food historian. I'm a farmer-founder following each ingredient back to where it began.
          Every article here traces one spice's history and origin, and links to the matching blend so you can taste
          it.
        </p>
      </div>

      <div className="mt-10 flex flex-col gap-3 sm:flex-row">
        <Link to="/encyclopedia" className="btn-dark">Start reading</Link>
        <a href="https://fudipeople.com" className="btn-outline">Visit the shop</a>
      </div>
    </div>
  )
}
