import { useEffect, useState } from 'react';
import { API_BASE_URL } from './api.js';
import LeagueSelector from './components/LeagueSelector.jsx';
import Scoreboard from './components/Scoreboard.jsx';

export default function App() {
  const [leagues, setLeagues] = useState([]);
  const [selectedLeague, setSelectedLeague] = useState(null);
  const [pollIntervalMs, setPollIntervalMs] = useState(120000);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function loadInitialData() {
      setLoading(true);
      setError(null);
      try {
        const [configRes, leaguesRes] = await Promise.all([
          fetch(`${API_BASE_URL}/config`),
          fetch(`${API_BASE_URL}/leagues`),
        ]);

        if (!configRes.ok) {
          throw new Error(`Failed to load config (status ${configRes.status})`);
        }
        if (!leaguesRes.ok) {
          throw new Error(`Failed to load leagues (status ${leaguesRes.status})`);
        }

        const configData = await configRes.json();
        const leaguesData = await leaguesRes.json();

        if (cancelled) return;

        const leagueList = leaguesData.leagues || [];
        setLeagues(leagueList);
        setPollIntervalMs(configData.poll_interval_ms || 120000);
        setSelectedLeague(
          leagueList.includes('nba') ? 'nba' : leagueList[0] || null
        );
      } catch (err) {
        if (!cancelled) {
          setError(err.message || 'Failed to load application data');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadInitialData();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="min-h-screen bg-espn-bg">
      <header className="border-b border-espn-border bg-espn-panel px-4 py-3 sm:px-6">
        <div className="mx-auto flex max-w-4xl items-center justify-between">
          <h1 className="text-xl font-bold tracking-tight text-white">
            ESPN Scoreboard
          </h1>
          {leagues.length > 0 && (
            <LeagueSelector
              leagues={leagues}
              selectedLeague={selectedLeague}
              onChange={setSelectedLeague}
            />
          )}
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-4 py-6 sm:px-6">
        {loading && (
          <p className="text-center text-gray-400">Loading application data…</p>
        )}
        {error && !loading && (
          <p className="rounded border border-red-800 bg-red-950/40 px-4 py-3 text-red-300">
            {error}
          </p>
        )}
        {!loading && !error && selectedLeague && (
          <Scoreboard league={selectedLeague} pollIntervalMs={pollIntervalMs} />
        )}
        {!loading && !error && !selectedLeague && (
          <p className="text-center text-gray-400">No leagues available.</p>
        )}
      </main>
    </div>
  );
}
