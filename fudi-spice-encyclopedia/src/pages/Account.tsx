import { useState } from 'react'
import { Link, Navigate } from 'react-router-dom'
import Seo from '../components/Seo'
import { useAuth } from '../context/AuthContext'
import { openCustomerPortal } from '../lib/api'

export default function Account() {
  const { session, profile, loading, isMember, signOut } = useAuth()
  const [error, setError] = useState<string | null>(null)

  if (loading) return <p className="container-page py-16">Loading…</p>
  if (!session) return <Navigate to="/login" replace state={{ from: '/account' }} />

  async function manage() {
    try {
      window.location.assign(await openCustomerPortal())
    } catch (e) {
      setError((e as Error).message)
    }
  }

  return (
    <div className="container-page max-w-xl py-14">
      <Seo title="Your account" />
      <h1 className="text-3xl font-extrabold text-maroon">Your account</h1>
      <dl className="mt-6 space-y-3 rounded-xl bg-white p-6 ring-1 ring-ink/10">
        <div><dt className="text-sm text-ink/70">Email</dt><dd className="font-semibold">{session.user.email}</dd></div>
        <div>
          <dt className="text-sm text-ink/70">Membership</dt>
          <dd className="font-semibold">{isMember ? 'Member' : 'Free'}</dd>
        </div>
        {profile?.current_period_end && isMember && (
          <div>
            <dt className="text-sm text-ink/70">Current period ends</dt>
            <dd className="font-semibold">{new Date(profile.current_period_end).toLocaleDateString('en-GB')}</dd>
          </div>
        )}
      </dl>
      <div className="mt-6 flex flex-wrap gap-3">
        {profile?.membership_status === 'member' ? (
          <button className="btn-dark" onClick={manage}>Manage or cancel membership</button>
        ) : (
          <Link to="/membership" className="btn-primary">Become a member</Link>
        )}
        <button className="btn-outline" onClick={signOut}>Sign out</button>
      </div>
      {error && <p role="alert" className="mt-4 font-semibold text-maroon">{error}</p>}
    </div>
  )
}
