import { NavLink, Outlet } from 'react-router-dom'

const tab = ({ isActive }: { isActive: boolean }) =>
  `rounded-full px-4 py-2 text-sm font-bold ${isActive ? 'bg-maroon text-cream' : 'bg-white ring-1 ring-ink/15'}`

export default function AdminLayout() {
  return (
    <div className="container-page py-10">
      <h1 className="text-3xl font-extrabold text-maroon">Admin</h1>
      <nav aria-label="Admin" className="mt-4 flex gap-2">
        <NavLink to="/admin" end className={tab}>Articles</NavLink>
        <NavLink to="/admin/products" className={tab}>Products</NavLink>
      </nav>
      <div className="mt-8">
        <Outlet />
      </div>
    </div>
  )
}
