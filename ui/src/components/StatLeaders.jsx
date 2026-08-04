export default function StatLeaders({ statLeaders, align = 'left' }) {
  if (!statLeaders || statLeaders.length === 0) {
    return null;
  }

  const alignClass = align === 'right' ? 'items-end text-right' : 'items-start text-left';

  return (
    <ul className={`flex flex-col gap-1 ${alignClass}`}>
      {statLeaders.map((leader, idx) => {
        const isOverallLeader = leader.isOverallLeader;
        return (
          <li key={idx} className="text-xs">
            <div className="font-medium text-espn-accent">{leader.label}</div>
            <div className={isOverallLeader ? 'font-bold text-espn-highlight' : 'text-gray-400'}>
              {leader.name}{' '}
              <span className={isOverallLeader ? 'text-espn-highlight' : 'text-gray-500'}>
                {leader.stat_value}
              </span>
            </div>
          </li>
        );
      })}
    </ul>
  );
}
