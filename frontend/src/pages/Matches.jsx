import { useEffect, useState } from 'react'
import api from '../api/client'

export default function Matches() {
  const [matches, setMatches] = useState([])
  const [myPredictions, setMyPredictions] = useState({})
  const [drafts, setDrafts] = useState({})
  const [message, setMessage] = useState('')

  async function loadData() {
    const [matchesRes, predsRes] = await Promise.all([
      api.get('/matches'),
      api.get('/matches/predictions/me'),
    ])
    setMatches(matchesRes.data)
    const predsByMatch = {}
    predsRes.data.forEach((p) => { predsByMatch[p.match_id] = p })
    setMyPredictions(predsByMatch)
  }

  useEffect(() => {
    loadData()
  }, [])

  function updateDraft(matchId, field, value) {
    setDrafts((prev) => ({
      ...prev,
      [matchId]: { ...prev[matchId], [field]: value },
    }))
  }

  async function submitPrediction(matchId) {
    const draft = drafts[matchId]
    if (!draft || draft.home_score_pred === undefined || draft.away_score_pred === undefined) return
    setMessage('')
    try {
      await api.post('/matches/predictions', {
        match_id: matchId,
        home_score_pred: Number(draft.home_score_pred),
        away_score_pred: Number(draft.away_score_pred),
      })
      setMessage('Prediccion guardada')
      loadData()
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Error al guardar la prediccion')
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Partidos</h1>
      {message && <p className="mb-4 text-sm text-green-700">{message}</p>}
      <div className="flex flex-col gap-4">
        {matches.map((match) => {
          const existing = myPredictions[match.id]
          const draft = drafts[match.id] || {}
          const finished = match.home_score_real !== null && match.away_score_real !== null

          return (
            <div key={match.id} className="bg-white rounded-lg shadow p-4">
              <p className="font-semibold">{match.home_team} vs {match.away_team}</p>
              <p className="text-xs text-slate-500 mb-3">
                {new Date(match.match_date).toLocaleString()}
              </p>

              {finished ? (
                <p className="text-sm">
                  Resultado real: <strong>{match.home_score_real} - {match.away_score_real}</strong>
                  {existing && (
                    <span className="ml-3">
                      Tu prediccion: {existing.home_score_pred} - {existing.away_score_pred} ·{' '}
                      <strong>{existing.points ?? 0} pts</strong>
                    </span>
                  )}
                </p>
              ) : (
                <div className="flex items-center gap-2">
                  <input
                    type="number"
                    min="0"
                    className="w-16 border rounded px-2 py-1"
                    placeholder={existing?.home_score_pred ?? '0'}
                    value={draft.home_score_pred ?? existing?.home_score_pred ?? ''}
                    onChange={(e) => updateDraft(match.id, 'home_score_pred', e.target.value)}
                  />
                  <span>-</span>
                  <input
                    type="number"
                    min="0"
                    className="w-16 border rounded px-2 py-1"
                    placeholder={existing?.away_score_pred ?? '0'}
                    value={draft.away_score_pred ?? existing?.away_score_pred ?? ''}
                    onChange={(e) => updateDraft(match.id, 'away_score_pred', e.target.value)}
                  />
                  <button
                    onClick={() => submitPrediction(match.id)}
                    className="ml-2 bg-slate-900 text-white text-sm px-3 py-1 rounded hover:bg-slate-700"
                  >
                    {existing ? 'Actualizar' : 'Predecir'}
                  </button>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
