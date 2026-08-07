import { useEffect } from 'react';

export default function Modal({ title, onClose, children }) {
  useEffect(() => {
    function handleKeyDown(e) {
      if (e.key === 'Escape') {
        onClose();
      }
    }
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4"
      onClick={onClose}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className="w-full max-w-sm rounded border border-espn-border bg-espn-panel p-4 shadow-lg"
        onClick={(e) => e.stopPropagation()}
      >
        {title && (
          <h2 className="mb-3 text-sm font-semibold text-white">{title}</h2>
        )}
        {children}
      </div>
    </div>
  );
}
