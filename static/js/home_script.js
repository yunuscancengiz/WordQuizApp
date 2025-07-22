(function applyInitialTheme() {
  const saved = localStorage.getItem("theme");
  if (saved === "dark") {
    document.body.classList.add("dark");
  }
})();

const COLORS = {
  primary: '#4361ee',
  secondary: '#f72585',
  highlight: '#4cc9f0',
  warning: '#ff9f1c',
  success: '#80ed99',
  danger: '#ef233c',
  lightGray: '#e0e0e0',
  darkGray: '#6c757d',
  vibrantGreen: '#38b000',
  vibrantRed: '#d00000'
};

new Chart(document.getElementById('quizChart'), {
  
  type: 'bar',
  data: {
    labels: ['Today'],
    datasets: [
      { label: 'Quiz Max Streak', data: [max_streak], backgroundColor: COLORS.primary, borderRadius: 6 },
      { label: 'Question Count', data: [today_question_count], backgroundColor: COLORS.warning, borderRadius: 6 }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      tooltip: {
        callbacks: { label: ctx => `${ctx.dataset.label}: ${ctx.raw}` },
        backgroundColor: '#222', titleColor: '#fff', bodyColor: '#fff'
      },
      legend: { position: 'bottom', labels: { color: COLORS.darkGray } }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { stepSize: 5, color: COLORS.darkGray },
        // grid: { color: COLORS.lightGray }
      }
    }
  }
});

window.addEventListener('DOMContentLoaded', () => {
  const ctx = document.getElementById('quizChart');
});
