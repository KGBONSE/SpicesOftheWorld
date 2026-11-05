import type { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

/** UI guard only. The real protection is RLS: non-admins cannot write or read bodies regardless. */
export default function RequireAdmin({ children }: { children: ReactNode }) {
  const { session, isAdmin, loading } = useAuth()
  if (loading) return <p className="container-page py-16">Loading…</p>
  if (!session) return <Navigate to="/login" replace state={{ from: '/admin' }} />
  if (!isAdmin) return <p className="container-page py-16">This area is for the site owner only.</p>
  return <>{children}</>
}
