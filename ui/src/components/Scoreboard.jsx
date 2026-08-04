import { useEffect, useState } from 'react';
import { API_BASE_URL } from '../api.js';
import GameCard from './GameCard.jsx';

function formatTimestamp(date) {
  return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
}

// Converts an <input type="date"> value ("YYYY-MM-DD") to the API's expected
// "YYYYMMDD" format.
function toApiDate(isoDate) {
  return isoDate ? isoDate.replaceAll('-', '') : null;
}

export default function Scoreboard({ league, date, pollIntervalMs }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchScoreboard() {
      try {
        const params = new URLSearchParams({ league });
        const apiDate = toApiDate(date);
        if (apiDate) {
          params.set('date', apiDate);
        }
        const res = await fetch(`${API_BASE_URL}/scoreboard?${params.toString()}`);
        const body = await res.json().catch(() => null);

        if (!res.ok) {
          const detail = body && body.detail ? body.detail : `Request failed (status ${res.status})`;
          throw new Error(detail);
        }

        if (cancelled) return;
        setData(body);
        setError(null);
        setLastUpdated(new Date());
      } catch (err) {
        if (!cancelled) {
          setError(err.message || 'Failed to load scoreboard');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    setLoading(true);
    setError(null);
    setData(null);
    fetchScoreboard();

    const intervalId = setInterval(fetchScoreboard, pollIntervalMs);

    return () => {
      cancelled = true;
      clearInterval(intervalId);
    };
  }, [league, date, pollIntervalMs]);

  if (loading) {
    return <p className="text-center text-gray-400">Loading scoreboard…</p>;
  }

  if (error) {
    return (
      <p className="rounded border border-red-800 bg-red-950/40 px-4 py-3 text-red-300">
        {error}
      </p>
    );
  }

  const games = data?.games || [];

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white">
          {data?.league} — {data?.date_display}
        </h2>
      </div>

      {games.length === 0 ? (
        <p className="text-center text-gray-400">No games scheduled.</p>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {games.map((game, idx) => (
            <GameCard key={`${game.title}-${idx}`} game={game} />
          ))}
        </div>
      )}

      {lastUpdated && (
        <p className="mt-6 text-center text-xs text-gray-500">
          Last updated: {formatTimestamp(lastUpdated)}
        </p>
      )}
    </div>
  );
}
