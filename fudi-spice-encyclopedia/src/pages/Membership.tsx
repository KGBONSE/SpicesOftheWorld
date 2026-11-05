import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Seo from '../components/Seo'
import { useAuth } from '../context/AuthContext'
import { startCheckout } from '../lib/api'

// Prices are display-only; the real amounts live in your Stripe Prices. Update both together.
const PLANS = [
  { id: 'monthly' as const, name: 'Monthly', price: '£X.XX / month', note: 'Cancel any time' },
  { id: 'annual' as const, name: 'Annual', price: '£XX.XX / year', note: 'Best value' },
]

export default function Membership() {
  const { session, isMember } = useAuth()
  const navigate = useNavigate()
  const [busy, setBusy] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function choose(plan: 'monthly' | 'annual') {
    if (!session) return navigate('/login', { state: { from: '/membership' } })
    setBusy(plan)
    setError(null)
    try {
      window.location.assign(await startCheckout(plan))
    } catch (e) {
      setError((e as Error).message)
      setBusy(null)
    }
  }

  return (
    <div className="container-page max-w-4xl py-14">
      <Seo title="Membership" description="Unlock every full article in the Fudi People Spice Encyclopedia." path="/membership" />
      <h1 className="text-4xl font-extrabold text-maroon">Membership</h1>
      <p className="mt-3 max-w-2xl text-lg">Unlock the full history and origin story of every spice in the encyclopedia.</p>

      {isMember ? (
        <p className="mt-8 rounded-xl bg-white p-5 font-semibold ring-1 ring-ink/10">You're already a member. Thank you.</p>
      ) : (
        <div className="mt-10 grid gap-6 sm:grid-cols-2">
          {PLANS.map((p) => (
            <section key={p.id} className="rounded-2xl bg-white p-7 ring-1 ring-ink/10">
              <h2 className="text-xl font-extrabold">{p.name}</h2>
              <p className="mt-2 text-2xl font-extrabold text-maroon">{p.price}</p>
              <p className="mt-1 text-sm text-ink/70">{p.note}</p>
              <button className="btn-primary mt-6 w-full" disabled={busy !== null} onClick={() => choose(p.id)}>
                {busy === p.id ? 'Redirecting…' : session ? `Join ${p.name.toLowerCase()}` : 'Sign in to join'}
              </button>
            </section>
          ))}
        </div>
      )}
      {error && <p role="alert" className="mt-4 font-semibold text-maroon">{error}</p>}
    </div>
  )
}
