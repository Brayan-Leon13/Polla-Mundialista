import { useEffect, useState } from 'react'
import api from '../api/client'

export default function Leaderboard() {
  const [entries, setEntries] = useState([])
  const [selectedUser, setSelectedUser] = useState(null)
  const [history, setHistory] = useState([])

  useEffect(() => {
    api.get('/leaderboard').then((res) => setEntries(res.data))
  }, [])

  async function showHistory(entry) {
    setSelectedUser(entry)
    const { data } = await api.get(`/users/${entry.user_id}/predictions`)
    setHistory(data)
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Ranking</h1>
      <table className="w-full bg-white rounded-lg shadow overflow-hidden">
        <thead className="bg-slate-100 text-left text-sm">
          <tr>
            <th className="p-3">#</th>
            <th className="p-3">Usuario</th>
            <th className="p-3">Puntos</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((entry, idx) => (
            <tr
              key={entry.user_id}
              className="border-t cursor-pointer hover:bg-slate-50"
              onClick={() => showHistory(entry)}
            >
              <td className="p-3">{idx + 1}</td>
              <td className="p-3">{entry.email}</td>
              <td className="p-3 font-semibold">{entry.total_points}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedUser && (
        <div className="mt-6 bg-white rounded-lg shadow p-4">
          <h2 className="font-semibold mb-3">Historial de {selectedUser.email}</h2>
          {history.length === 0 ? (
            <p className="text-sm text-slate-500">Sin predicciones todavia.</p>
          ) : (
            <ul className="text-sm flex flex-col gap-1">
              {history.map((p) => (
                <li key={p.id}>
                  Partido #{p.match_id}: predijo {p.home_score_pred}-{p.away_score_pred}
                  {p.points !== null && <> · {p.points} pts</>}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  )
}
