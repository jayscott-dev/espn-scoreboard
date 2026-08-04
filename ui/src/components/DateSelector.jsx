export default function DateSelector({ selectedDate, onChange }) {
  return (
    <div className="flex items-center gap-2">
      <input
        type="date"
        className="rounded border border-espn-border bg-espn-card px-3 py-1.5 text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-espn-accent"
        value={selectedDate || ''}
        onChange={(e) => onChange(e.target.value || null)}
        aria-label="Select date"
      />
      {selectedDate && (
        <button
          type="button"
          className="rounded border border-espn-border bg-espn-card px-3 py-1.5 text-sm font-medium text-white hover:bg-espn-panel focus:outline-none focus:ring-2 focus:ring-espn-accent"
          onClick={() => onChange(null)}
        >
          Today
        </button>
      )}
    </div>
  );
}
