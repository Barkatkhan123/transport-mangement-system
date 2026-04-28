document.addEventListener('DOMContentLoaded', () => {

  // ── Minimum date for date inputs ────────────────────────
  const today = new Date().toISOString().split('T')[0];
  document.querySelectorAll('input[type="date"]').forEach(input => {
    if (!input.min) input.min = today;
  });

  // ── Confirm delete actions ──────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', e => {
      if (!confirm(el.dataset.confirm)) e.preventDefault();
    });
  });

});
