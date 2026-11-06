import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Paywall() {
  const { session } = useAuth()
  const { pathname } = useLocation()
  return (
    <section
      aria-labelledby="paywall-heading"
      className="relative mx-auto -mt-24 max-w-[68ch] bg-gradient-to-t from-cream via-cream to-transparent pt-24"
    >
      <div className="rounded-2xl bg-maroon p-7 text-center text-cream shadow-lg sm:p-9">
        <h2 id="paywall-heading" className="text-2xl font-extrabold">
          Keep reading with a Fudi membership
        </h2>
        <p className="mx-auto mt-3 max-w-md text-cream/85">
          Full histories and origin stories for every spice in the encyclopedia, from a farmer who grows the chillies himself.
        </p>
        <div className="mt-6 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Link to="/membership" className="btn-primary">See membership</Link>
          {!session && (
            <Link to="/login" state={{ from: pathname }} className="btn border-2 border-cream/40 hover:border-cream">
              I have an account
            </Link>
          )}
        </div>
      </div>
    </section>
  )
}
