import { useState, type FormEvent } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import Seo from '../components/Seo'
import { useAuth } from '../context/AuthContext'
import { isConfigured, SITE_URL, supabase } from '../lib/supabase'

type Mode = 'signin' | 'signup' | 'magic'

export default function Login() {
  const [mode, setMode] = useState<Mode>('signin')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState<{ kind: 'error' | 'ok'; text: string } | null>(null)
  const { session } = useAuth()
  const navigate = useNavigate()
  const from = (useLocation().state as { from?: string } | null)?.from ?? '/account'

  if (session) return <Navigate to={from} replace />

  async function submit(e: FormEvent) {
    e.preventDefault()
    if (!supabase) return
    setBusy(true)
    setMessage(null)
    try {
      if (mode === 'magic') {
        const { error } = await supabase.auth.signInWithOtp({ email, options: { emailRedirectTo: `${SITE_URL}${from}` } })
        if (error) throw error
        setMessage({ kind: 'ok', text: 'Check your email for a sign-in link.' })
      } else if (mode === 'signup') {
        const { data, error } = await supabase.auth.signUp({ email, password, options: { emailRedirectTo: `${SITE_URL}${from}` } })
        if (error) throw error
        if (data.session) navigate(from, { replace: true })
        else setMessage({ kind: 'ok', text: 'Account created. Check your email to confirm it, then sign in.' })
      } else {
        const { error } = await supabase.auth.signInWithPassword({ email, password })
        if (error) throw error
      }
    } catch (err) {
      setMessage({ kind: 'error', text: (err as Error).message })
    } finally {
      setBusy(false)
    }
  }

  const title = mode === 'signup' ? 'Create your account' : 'Sign in'

  return (
    <div className="container-page max-w-md py-14">
      <Seo title={title} />
      <h1 className="text-3xl font-extrabold text-maroon">{title}</h1>

      {!isConfigured && (
        <p className="mt-4 rounded-lg bg-cream-dark p-3 text-sm">Sign-in needs Supabase keys in .env.local.</p>
      )}

      <form onSubmit={submit} className="mt-6 space-y-4">
        <div>
          <label htmlFor="email" className="label">Email</label>
          <input id="email" type="email" required autoComplete="email" className="field" value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
        {mode !== 'magic' && (
          <div>
            <label htmlFor="password" className="label">Password</label>
            <input
              id="password"
              type="password"
              required
              minLength={8}
              autoComplete={mode === 'signup' ? 'new-password' : 'current-password'}
              className="field"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        )}
        <button type="submit" disabled={busy || !isConfigured} className="btn-dark w-full disabled:opacity-60">
          {busy ? 'Please wait…' : mode === 'magic' ? 'Email me a magic link' : title}
        </button>
        {message && (
          <p role={message.kind === 'error' ? 'alert' : 'status'} className={message.kind === 'error' ? 'font-semibold text-maroon' : 'font-semibold'}>
            {message.text}
          </p>
        )}
      </form>

      <div className="mt-6 flex flex-col gap-2 text-sm">
        {mode !== 'magic' && <button className="text-left underline" onClick={() => setMode('magic')}>Use a magic link instead</button>}
        {mode !== 'signin' && <button className="text-left underline" onClick={() => setMode('signin')}>Sign in with password</button>}
        {mode !== 'signup' && <button className="text-left underline" onClick={() => setMode('signup')}>New here? Create an account</button>}
      </div>
    </div>
  )
}
