import { useState } from 'react'
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom'
import { useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { isConfigured } from '../lib/supabase'

const navLink = ({ isActive }: { isActive: boolean }) =>
  `rounded px-2 py-2 text-sm font-semibold hover:text-marigold ${isActive ? 'text-marigold' : ''}`

export default function Layout() {
  const [open, setOpen] = useState(false)
  const { session, isAdmin } = useAuth()
  const { pathname } = useLocation()

  useEffect(() => {
    setOpen(false)
    window.scrollTo(0, 0)
  }, [pathname])

  return (
    <div className="flex min-h-screen flex-col">
      <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:bg-cream focus:p-3">
        Skip to content
      </a>
      {!isConfigured && (
        <p className="bg-marigold px-4 py-2 text-center text-xs font-semibold text-ink">
          Preview mode: showing placeholder content. Add Supabase keys to .env.local to go live.
        </p>
      )}
      <header className="bg-maroon text-cream">
        <div className="container-page flex h-16 items-center justify-between">
          <Link to="/" className="text-lg font-extrabold tracking-tight">
            Fudi People <span className="text-gold">Spice Encyclopedia</span>
          </Link>
          <button
            className="rounded p-2 md:hidden"
            aria-expanded={open}
            aria-controls="main-nav"
            onClick={() => setOpen(!open)}
          >
            <span className="sr-only">Menu</span>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              {open ? <path d="M6 6l12 12M18 6L6 18" /> : <path d="M4 7h16M4 12h16M4 17h16" />}
            </svg>
          </button>
          <nav
            id="main-nav"
            aria-label="Main"
            className={`${open ? 'flex' : 'hidden'} absolute inset-x-0 top-16 z-30 flex-col gap-1 bg-maroon px-5 pb-4 md:static md:flex md:flex-row md:items-center md:gap-3 md:bg-transparent md:p-0`}
          >
            <NavLink to="/encyclopedia" className={navLink}>Encyclopedia</NavLink>
            <NavLink to="/about" className={navLink}>About Kofi</NavLink>
            <NavLink to="/membership" className={navLink}>Membership</NavLink>
            {isAdmin && <NavLink to="/admin" className={navLink}>Admin</NavLink>}
            {session ? (
              <NavLink to="/account" className={navLink}>Account</NavLink>
            ) : (
              <Link to="/login" className="btn-primary mt-2 md:mt-0">Sign in</Link>
            )}
          </nav>
        </div>
      </header>

      <main id="main" className="flex-1">
        <Outlet />
      </main>

      <footer className="bg-ink text-cream">
        <div className="container-page grid gap-6 py-10 text-sm sm:grid-cols-2">
          <div>
            <p className="font-extrabold">Fudi People</p>
            <p className="mt-2 max-w-sm text-cream/80">
              Small-batch spice blends and vegan chilli oil, made with chillies grown on our farm in Sidcup, London.
            </p>
          </div>
          <ul className="flex flex-wrap gap-x-6 gap-y-2 sm:justify-end">
            <li><Link to="/encyclopedia" className="hover:text-gold">Encyclopedia</Link></li>
            <li><Link to="/membership" className="hover:text-gold">Membership</Link></li>
            <li><Link to="/about" className="hover:text-gold">About</Link></li>
            <li><a href="https://fudipeople.com" className="hover:text-gold">Shop</a></li>
          </ul>
        </div>
      </footer>
    </div>
  )
}
