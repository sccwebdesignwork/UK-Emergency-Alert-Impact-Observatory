'use strict';
// Status-only evidence; no public scientific estimates are rendered.
(async function status() {
  const target = document.querySelector('[data-updated]');
  if (!target) return;
  try {
    const response = await fetch('data/evidence.json', {cache: 'no-store'});
    if (!response.ok) throw new Error('status unavailable');
    const record = await response.json();
    if (record.study_status !== 'methodology_under_independent_review' ||
        record.publication_approved !== false ||
        record.causal_claim_allowed !== false ||
        !Array.isArray(record.historical_results) ||
        record.historical_results.length !== 0 ||
        record.scientific_results_status !== 'withheld_pending_independent_review') {
      throw new Error('scientific publication not authorised');
    }
    if (typeof record.status_reviewed_at === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(record.status_reviewed_at)) {
      const [y, m, d] = record.status_reviewed_at.split('-').map(Number);
      if (m >= 1 && m <= 12 && d >= 1 && d <= 31) {
        target.textContent = d + ' ' + ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m-1] + ' ' + y;
      }
    }
  } catch (_) {
    target.textContent = 'Status readback unavailable';
  }
})();
