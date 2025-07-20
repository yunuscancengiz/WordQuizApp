(function applyInitialTheme() {
  const saved = localStorage.getItem("theme");
  if (saved === "dark") {
    document.body.classList.add("dark");
  }
})();

// Mock data
const labels = [
  '2025-06-22', '2025-06-23', '2025-06-24', '2025-06-25',
  '2025-06-26', '2025-06-27', '2025-06-28',
  '2025-06-30', '2025-07-01', '2025-07-02',
  '2025-07-03', '2025-07-04', '2025-07-05',
  '2025-07-06', '2025-07-07'
];

const data = {
  labels: labels,
  datasets: [{
    label: 'Daily Max Streak',
    data: [15, 22, 18, 33, 25, 26, 27, 8, 32, 34, 36, 21, 40, 38, 37],
    fill: false,
    borderColor: '#ffffffff',
    tension: 0.2,
    pointHoverRadius: 20
  }]
};

const config = {
  type: 'line',
  data: data,
  options: {
    plugins: {
      tooltip: {
        callbacks: {
          label: (context) => ` ${context.raw} max streak`
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Max Streak' }
      },
      x: {
        title: { display: true, text: 'Date' }
      }
    },
    responsive: true,
    maintainAspectRatio: false
  }
};

window.addEventListener('DOMContentLoaded', () => {
  const ctx = document.getElementById('streakChart');
  new Chart(ctx, config);
});
