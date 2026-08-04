import StatLeaders from './StatLeaders.jsx';

// Extracts the leading numeric portion of a stat value string (e.g. "0.000 (0-1)" -> 0).
function parseStatValue(statValue) {
  const match = /-?\d+(\.\d+)?/.exec(statValue ?? '');
  return match ? parseFloat(match[0]) : Number.NEGATIVE_INFINITY;
}

// Splits stat leaders into away/home side lists. Every leader stays on its own
// team's side. For each stat label present on both sides, the entry with the
// higher value is flagged `isOverallLeader` so it can be visually highlighted.
function splitLeaders(leaders, awayTeamId, homeTeamId) {
  const byLabel = new Map();

  for (const leader of leaders) {
    if (leader.team_id !== awayTeamId && leader.team_id !== homeTeamId) {
      continue;
    }
    const side = leader.team_id === awayTeamId ? 'away' : 'home';
    if (!byLabel.has(leader.label)) {
      byLabel.set(leader.label, { away: [], home: [] });
    }
    byLabel.get(leader.label)[side].push(leader);
  }

  const awayLeaders = [];
  const homeLeaders = [];

  for (const { away, home } of byLabel.values()) {
    let awayIsOverall = false;
    let homeIsOverall = false;

    if (away.length > 0 && home.length > 0) {
      const awayValue = parseStatValue(away[0].stat_value);
      const homeValue = parseStatValue(home[0].stat_value);
      awayIsOverall = awayValue >= homeValue;
      homeIsOverall = !awayIsOverall;
    }

    awayLeaders.push(...away.map((leader) => ({ ...leader, isOverallLeader: awayIsOverall })));
    homeLeaders.push(...home.map((leader) => ({ ...leader, isOverallLeader: homeIsOverall })));
  }

  return { awayLeaders, homeLeaders };
}

function TeamHeader({ team, align }) {
  const alignClass = align === 'right' ? 'items-end text-right' : 'items-start text-left';
  return (
    <div className={`flex flex-col ${alignClass}`}>
      <span className="font-semibold text-white">{team.name}</span>
      {team.record ? (
        <span className="text-xs text-gray-500">({team.record})</span>
      ) : null}
    </div>
  );
}

export default function GameCard({ game }) {
  const {
    title,
    start_time: startTime,
    status,
    status_detail: statusDetail,
    series_info: seriesInfo,
    home_team: homeTeam,
    away_team: awayTeam,
    stat_leaders: statLeaders,
  } = game;

  const { awayLeaders, homeLeaders } = splitLeaders(
    statLeaders || [],
    awayTeam.id,
    homeTeam.id
  );

  return (
    <div className="rounded-lg border border-espn-border bg-espn-card p-4 shadow">
      <div className="mb-2 flex items-center justify-between">
        <span className="text-xs uppercase tracking-wide text-gray-400">
          {startTime}
        </span>
        <span className="rounded bg-espn-panel px-2 py-0.5 text-xs font-semibold text-espn-accent">
          {status}
        </span>
      </div>

      <h3 className="mb-2 text-sm text-gray-300">{title}</h3>

      {statusDetail ? (
        <p className="mb-2 text-xs text-gray-500">{statusDetail}</p>
      ) : null}

      <div className="grid grid-cols-3 items-start gap-2">
        <TeamHeader team={awayTeam} align="left" />
        <div className="flex justify-center gap-3 text-2xl font-bold text-white">
          <span>{awayTeam.score}</span>
          <span className="text-gray-500">-</span>
          <span>{homeTeam.score}</span>
        </div>
        <TeamHeader team={homeTeam} align="right" />
      </div>

      {seriesInfo ? (
        <p className="mt-2 text-xs italic text-gray-500">{seriesInfo}</p>
      ) : null}

      {(awayLeaders.length > 0 || homeLeaders.length > 0) ? (
        <div className="mt-3 grid grid-cols-3 items-start gap-2 border-t border-espn-border pt-2">
          <div className="col-start-1">
            <StatLeaders statLeaders={awayLeaders} align="left" />
          </div>
          <div className="col-start-3">
            <StatLeaders statLeaders={homeLeaders} align="right" />
          </div>
        </div>
      ) : null}
    </div>
  );
}
