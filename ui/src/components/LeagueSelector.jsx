export default function LeagueSelector({ leagues, selectedLeague, onChange }) {
  return (
    <select
      className="rounded border border-espn-border bg-espn-card px-3 py-1.5 text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-espn-accent"
      value={selectedLeague || ''}
      onChange={(e) => onChange(e.target.value)}
      aria-label="Select league"
    >
      {leagues.map((league) => (
        <option key={league} value={league}>
          {league.toUpperCase()}
        </option>
      ))}
    </select>
  );
}
