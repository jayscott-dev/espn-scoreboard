import { useState } from 'react';
import Modal from './Modal.jsx';

function formatDisplayDate(isoDate) {
  const [year, month, day] = isoDate.split('-').map(Number);
  return new Date(year, month - 1, day).toLocaleDateString([], {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

export default function DateSelector({ selectedDate, onChange }) {
  const [isOpen, setIsOpen] = useState(false);
  const [pendingDate, setPendingDate] = useState(selectedDate || '');

  function openModal() {
    setPendingDate(selectedDate || '');
    setIsOpen(true);
  }

  function closeModal() {
    setIsOpen(false);
  }

  // Only fetches happen if the user confirms a date selection here — the
  // date input's onChange only updates local pending state until then.
  function handleApply() {
    onChange(pendingDate || null);
    closeModal();
  }

  function handleToday() {
    onChange(null);
    closeModal();
  }

  return (
    <>
      <button
        type="button"
        className="rounded border border-espn-border bg-espn-card px-3 py-1.5 text-sm font-medium text-white hover:bg-espn-panel focus:outline-none focus:ring-2 focus:ring-espn-accent"
        onClick={openModal}
      >
        {selectedDate ? formatDisplayDate(selectedDate) : 'Today'}
      </button>

      {isOpen && (
        <Modal title="Select a date" onClose={closeModal}>
          <div className="flex flex-col gap-4">
            <input
              type="date"
              autoFocus
              className="rounded border border-espn-border bg-espn-card px-3 py-1.5 text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-espn-accent"
              value={pendingDate}
              onChange={(e) => setPendingDate(e.target.value)}
              aria-label="Select date"
            />

            <div className="flex items-center justify-between gap-2">
              <button
                type="button"
                className="rounded border border-espn-border bg-espn-card px-3 py-1.5 text-sm font-medium text-white hover:bg-espn-panel focus:outline-none focus:ring-2 focus:ring-espn-accent"
                onClick={handleToday}
              >
                Today
              </button>

              <div className="flex gap-2">
                <button
                  type="button"
                  className="rounded border border-espn-border px-3 py-1.5 text-sm font-medium text-gray-300 hover:bg-espn-panel focus:outline-none focus:ring-2 focus:ring-espn-accent"
                  onClick={closeModal}
                >
                  Cancel
                </button>
                <button
                  type="button"
                  disabled={!pendingDate}
                  className="rounded border border-espn-border bg-espn-accent px-3 py-1.5 text-sm font-medium text-black hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-espn-accent disabled:cursor-not-allowed disabled:opacity-50"
                  onClick={handleApply}
                >
                  Apply
                </button>
              </div>
            </div>
          </div>
        </Modal>
      )}
    </>
  );
}
