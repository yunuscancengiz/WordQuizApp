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

const streakChart = new Chart(document.getElementById('streakChart'), {
  type: 'line',
  data: {
    labels: dashboardData.daily_streaks_dates,
    datasets: [
      {
        label: '🔥 Max Streak',
        data: dashboardData.daily_streaks_max,
        borderColor: COLORS.primary,
        backgroundColor: COLORS.primary,
        tension: 0.4,
        fill: false,
        pointRadius: 3,
        pointHoverRadius: 7,
        yAxisID: 'y'
      },
      {
        label: '❓ Questions',
        data: dashboardData.daily_streaks_question_count,
        borderColor: COLORS.warning,
        backgroundColor: COLORS.warning,
        tension: 0.4,
        fill: false,
        pointRadius: 3,
        pointHoverRadius: 7,
        yAxisID: 'y1'
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    scales: {
      x: {
        ticks: { color: COLORS.darkGray, maxRotation: 45, minRotation: 45 },
        // grid: { color: COLORS.lightGray }
      },
      y: {
        beginAtZero: true,
        ticks: { color: COLORS.primary },
        // grid: { color: COLORS.lightGray },
        title: { display: true, text: 'Max Streak', color: COLORS.primary },
        position: 'left'
      },
      y1: {
        beginAtZero: true,
        ticks: { color: COLORS.warning },
        grid: { drawOnChartArea: false },
        title: { display: true, text: 'Question Count', color: COLORS.warning },
        position: 'right'
      }
    },
    plugins: {
      tooltip: { backgroundColor: '#222', titleColor: '#fff', bodyColor: '#fff' },
      legend: { labels: { color: COLORS.darkGray } }
    }
  }
});

function scrollToToday() {
  const container = document.getElementById('streakChart').parentElement.parentElement;
  container.scrollLeft = container.scrollWidth;
}

new Chart(document.getElementById('accuracyChart'), {
  type: 'doughnut',
  data: {
    labels: ['Correct', 'Incorrect'],
    datasets: [{
      label: 'Answer Accuracy',
      data: [dashboardData.correct_total, dashboardData.incorrect_total],
      backgroundColor: [COLORS.vibrantGreen, COLORS.vibrantRed],
      borderRadius: 6
    }]
  },
  options: {
    responsive: true,
    plugins: {
      tooltip: { backgroundColor: '#222', titleColor: '#fff', bodyColor: '#fff' },
      legend: { labels: { color: COLORS.darkGray }, position: 'bottom' }
    }
  }
});

new Chart(document.getElementById('quizChart'), {
  type: 'bar',
  data: {
    labels: ['Today'],
    datasets: [
      { label: 'Quiz Max Streak', data: [dashboardData.quiz_max_streak], backgroundColor: COLORS.primary, borderRadius: 6 },
      { label: 'Question Count', data: [dashboardData.quiz_question_count], backgroundColor: COLORS.warning, borderRadius: 6 }
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

new Chart(document.getElementById('hardestWordsChart'), {
  type: 'bar',
  data: {
    labels: dashboardData.hardest_words_labels,
    datasets: [
      { label: 'Incorrect', data: dashboardData.hardest_words_incorrect, backgroundColor: COLORS.vibrantRed, borderRadius: 6 },
      { label: 'Correct', data: dashboardData.hardest_words_correct, backgroundColor: COLORS.vibrantGreen, borderRadius: 6 }
    ]
  },
  options: {
    responsive: true,
    indexAxis: 'y',
    scales: {
      x: { stacked: true, max: 45, ticks: { color: COLORS.darkGray } },
      y: { stacked: true, ticks: { color: COLORS.darkGray } }
    },
    plugins: {
      tooltip: {
        callbacks: {
          label: ctx => `${ctx.dataset.label}: ${ctx.raw}${ctx.raw >= 15 ? ' (capped)' : ''}`
        },
        backgroundColor: '#222',
        titleColor: '#fff',
        bodyColor: '#fff'
      },
      legend: { labels: { color: COLORS.darkGray } }
    }
  }
});

new Chart(document.getElementById('mostCorrectWordsChart'), {
  type: 'bar',
  data: {
    labels: dashboardData.most_correct_words_labels,
    datasets: [{
      label: 'Correct Count',
      data: dashboardData.most_correct_words_data,
      backgroundColor: COLORS.success,
      borderRadius: 6
    }]
  },
  options: {
    responsive: true,
    indexAxis: 'y',
    scales: {
      x: { beginAtZero: true, ticks: { color: COLORS.darkGray } },
      y: { ticks: { color: COLORS.darkGray } }
    },
    plugins: {
      tooltip: { backgroundColor: '#222', titleColor: '#fff', bodyColor: '#fff' },
      legend: { labels: { color: COLORS.darkGray } }
    }
  }
});
