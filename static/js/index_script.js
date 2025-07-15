function toggleDarkMode() {
  document.body.classList.toggle("dark");
  localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
}

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
    borderColor: 'rgb(224, 21, 21)',
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



// logout, login, register functions

// Login JS
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);

        const payload = new URLSearchParams();
        for (const [key, value] of formData.entries()) {
            payload.append(key, value);
        }

        try {
            const response = await fetch('/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: payload.toString()
            });

            if (response.ok) {
                // Handle success (e.g., redirect to dashboard)
                const data = await response.json();
                // Delete any cookies available
                logout();
                // Save token to cookie
                document.cookie = `access_token=${data.access_token}; path=/`;
                window.location.href = '/'; // Change this to your desired redirect page
            } else {
                // Handle error
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}

// Register
const registerForm = document.getElementById('registerForm');
if (registerForm) {
  registerForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    if (data.password !== data.password2) {
      alert("Passwords do not match");
      return;
    }

    const payload = {
      email: data.email,
      username: data.username,
      first_name: data.first_name,
      last_name: data.last_name,
      password: data.password,
      role: data.role
    };

    try {
      const response = await fetch('/auth', {
        method: 'POST',
        headers:{
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        window.location.href = "{{ url_for('login-page') }}";
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occured. Please try again.');
    }
    
  });
}




// Logout 
function logout() {
  const cookies = document.cookie.split(";");

  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i];
    const eqPos = cookie.indexOf("=");
    const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;

    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
  }
  window.location.href = '/auth/login-page'
};


// function toggleDarkMode() {
//   const html = document.documentElement;
//   html.classList.toggle("dark");
//   localStorage.setItem("theme", html.classList.contains("dark") ? "dark" : "light");
// }