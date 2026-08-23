import { useEffect, useState } from 'react'
import api from '../api/client'

export default function Admin() {
  const [matches, setMatches] = useState([])
  const [drafts, setDrafts] = useState({})
  const [message, setMessage] = useState('')

  async function loadMatches() {
    const { data } = await api.get('/matches')
    setMatches(data)
  }

  useEffect(() => {
    loadMatches()
  }, [])

  function updateDraft(matchId, field, value) {
    setDrafts((prev) => ({
      ...prev,
      [matchId]: { ...prev[matchId], [field]: value },
    }))
  }

  async function saveResult(matchId) {
    const draft = drafts[matchId]
    if (!draft || draft.home_score_real === undefined || draft.away_score_real === undefined) return
    setMessage('')
    try {
      await api.put(`/admin/matches/${matchId}/result`, {
        home_score_real: Number(draft.home_score_real),
        away_score_real: Number(draft.away_score_real),
      })
      setMessage(`Resultado guardado para el partido ${matchId}`)
      loadMatches()
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Error al guardar el resultado')
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Panel de Administracion</h1>
      {message && <p className="mb-4 text-sm text-green-700">{message}</p>}
      <div className="flex flex-col gap-3">
        {matches.map((match) => (
          <div key={match.id} className="bg-white rounded-lg shadow p-4 flex items-center justify-between">
            <div>
              <p className="font-semibold">{match.home_team} vs {match.away_team}</p>
              {match.home_score_real !== null && (
                <p className="text-xs text-slate-500">
                  Resultado actual: {match.home_score_real} - {match.away_score_real}
                </p>
              )}
            </div>
            <div className="flex items-center gap-2">
              <input
                type="number"
                min="0"
                className="w-16 border rounded px-2 py-1"
                onChange={(e) => updateDraft(match.id, 'home_score_real', e.target.value)}
              />
              <span>-</span>
              <input
                type="number"
                min="0"
                className="w-16 border rounded px-2 py-1"
                onChange={(e) => updateDraft(match.id, 'away_score_real', e.target.value)}
              />
              <button
                onClick={() => saveResult(match.id)}
                className="ml-2 bg-slate-900 text-white text-sm px-3 py-1 rounded hover:bg-slate-700"
              >
                Guardar
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
