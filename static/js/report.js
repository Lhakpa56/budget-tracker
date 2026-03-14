document.addEventListener('DOMContentLoaded', () => {
  const raw = document.getElementById('chartData');
  if (!raw) return;

  const data = JSON.parse(raw.textContent);
  const { monthly, categories } = data;

  const INCOME  = '#3a7c5a';
  const EXPENSE = '#c94040';
  const GRID    = '#e8e4dc';
  const TEXT    = '#7a756c';
  const PALETTE = ['#c97d3a','#3a7c5a','#4a6fc9','#9b59b6','#e67e22','#1abc9c','#e74c3c','#3498db'];

  Chart.defaults.font.family = "'DM Sans', sans-serif";
  Chart.defaults.color = TEXT;

  // Bar chart — income vs expenses per month
  const barCtx = document.getElementById('barChart');
  if (barCtx) {
    new Chart(barCtx, {
      type: 'bar',
      data: {
        labels: monthly.map(m => m.month_name),
        datasets: [
          { label: 'Income',   data: monthly.map(m => m.income),   backgroundColor: INCOME  + 'cc', borderRadius: 4 },
          { label: 'Expenses', data: monthly.map(m => m.expenses), backgroundColor: EXPENSE + 'cc', borderRadius: 4 },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          tooltip: { callbacks: { label: ctx => ` $${ctx.parsed.y.toFixed(2)}` } },
        },
        scales: {
          x: { grid: { color: GRID } },
          y: { grid: { color: GRID }, ticks: { callback: v => `$${v}` } },
        },
      },
    });
  }

  // Doughnut chart — spending by category
  const doughnutCtx = document.getElementById('doughnutChart');
  if (doughnutCtx && categories.length) {
    new Chart(doughnutCtx, {
      type: 'doughnut',
      data: {
        labels: categories.map(c => c.name),
        datasets: [{
          data: categories.map(c => parseFloat(c.total)),
          backgroundColor: categories.map((_, i) => PALETTE[i % PALETTE.length]),
          borderWidth: 2,
          borderColor: '#fff',
        }],
      },
      options: {
        responsive: true,
        cutout: '62%',
        plugins: {
          legend: { position: 'right' },
          tooltip: { callbacks: { label: ctx => ` ${ctx.label}: $${ctx.parsed.toFixed(2)}` } },
        },
      },
    });
  }
});
