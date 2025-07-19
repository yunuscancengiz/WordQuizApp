// // Sayfa yüklenmeden önce dark mode sınıfını ekle
// (function applySavedThemeEarly() {
//   const savedTheme = localStorage.getItem("theme");
//   if (savedTheme === "dark") {
//     document.documentElement.classList.add("dark");
//   } else {
//     document.documentElement.classList.remove("dark");
//   }
// })();

// // Toggle butonuna basıldığında dark/light değiştir
// function toggleDarkMode() {
//   const html = document.documentElement;
//   const isDark = html.classList.contains("dark");

//   if (isDark) {
//     html.classList.remove("dark");
//     localStorage.setItem("theme", "light");
//   } else {
//     html.classList.add("dark");
//     localStorage.setItem("theme", "dark");
//   }

//   // Yeniden applyThemeColors çağrılarak renkler doğru uygulanır
//   applyStoredThemeColors();
// }

// // Sayfa yüklendikten sonra kaydedilen tema renklerini uygula
// document.addEventListener("DOMContentLoaded", () => {
//   applyStoredThemeColors();
// });

// function applyStoredThemeColors() {
//   const theme = JSON.parse(localStorage.getItem("activeTheme"));
//   if (theme) {
//     document.documentElement.style.setProperty("--darkcolor", theme.darkcolor);
//     document.documentElement.style.setProperty("--midcolor", theme.midcolor);
//     document.documentElement.style.setProperty("--lightcolor", theme.lightcolor);
//   }
// }


function toggleDarkMode() {
  const html = document.documentElement;
  const isDark = html.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

window.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('theme');
  const prefers = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  document.documentElement.classList.add(saved || prefers);
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
    console.log(payload)

    try {
      const response = await fetch('/auth', {
        method: 'POST',
        headers:{
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        window.location.href = '/auth/login-page';
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


// Helper function to get a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};