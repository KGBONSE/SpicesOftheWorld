import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="container-page py-24 text-center">
      <h1 className="text-4xl font-extrabold text-maroon">Page not found</h1>
      <p className="mt-3">That page isn't in the encyclopedia.</p>
      <Link to="/encyclopedia" className="btn-dark mt-6">Browse the encyclopedia</Link>
    </div>
  )
}
