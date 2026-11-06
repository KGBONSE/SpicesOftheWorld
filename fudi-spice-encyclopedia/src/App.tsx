import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import RequireAdmin from './components/RequireAdmin'
import Home from './pages/Home'
import Encyclopedia from './pages/Encyclopedia'
import ArticlePage from './pages/ArticlePage'
import About from './pages/About'
import Login from './pages/Login'
import Membership from './pages/Membership'
import Account from './pages/Account'
import NotFound from './pages/NotFound'
import AdminLayout from './pages/admin/AdminLayout'
import AdminArticles from './pages/admin/AdminArticles'
import AdminArticleEdit from './pages/admin/AdminArticleEdit'
import AdminProducts from './pages/admin/AdminProducts'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="encyclopedia" element={<Encyclopedia />} />
        <Route path="encyclopedia/:slug" element={<ArticlePage />} />
        <Route path="about" element={<About />} />
        <Route path="login" element={<Login />} />
        <Route path="membership" element={<Membership />} />
        <Route path="account" element={<Account />} />
        <Route
          path="admin"
          element={
            <RequireAdmin>
              <AdminLayout />
            </RequireAdmin>
          }
        >
          <Route index element={<AdminArticles />} />
          <Route path="articles/new" element={<AdminArticleEdit />} />
          <Route path="articles/:id" element={<AdminArticleEdit />} />
          <Route path="products" element={<AdminProducts />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}
