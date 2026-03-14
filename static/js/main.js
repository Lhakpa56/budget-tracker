document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss flash messages after 4 seconds
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity .4s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });

  // Default all date inputs to today if empty
  document.querySelectorAll('input[type="date"]').forEach(input => {
    if (!input.value) {
      input.value = new Date().toISOString().split('T')[0];
    }
  });
});
