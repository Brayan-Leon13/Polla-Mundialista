import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, isAdmin, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-slate-900 text-white px-6 py-4 flex items-center justify-between">
      <Link to="/" className="font-bold text-lg">Polla Mundialista</Link>
      <div className="flex items-center gap-4 text-sm">
        {user && <Link to="/">Partidos</Link>}
        {user && <Link to="/leaderboard">Ranking</Link>}
        {isAdmin && <Link to="/admin">Admin</Link>}
        {user ? (
          <>
            <span className="text-slate-300">{user.email}</span>
            <button onClick={handleLogout} className="bg-slate-700 px-3 py-1 rounded hover:bg-slate-600">
              Salir
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Registro</Link>
          </>
        )}
      </div>
    </nav>
  )
}
