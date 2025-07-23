# 🇫🇷 OuiChérie – Your Fun & Smart French Learning App

**OuiChérie** is an interactive, gamified French learning platform built with FastAPI and vanilla JavaScript. Designed to help users master vocabulary, sentence structure, and verb conjugations while keeping track of their daily progress through streaks and visualizations.

Now fully deployed and live!

---

## 🚀 Features

### 🔡 Flashcards
- Personalized flashcards based on user's vocabulary
- Enter the meaning manually to test recall
- Instant feedback and example sentence display
- Streak system: correct answers increase streak, wrong answers reset it

### 🔄 Quiz Mode
- Multiple choice questions (1 correct + 3 user-specific wrong choices)
- Randomized options each time
- Submit & Next flow with feedback and streak tracking

### 🧩 ROS – Randomly Ordered Sentences
- Arrange shuffled words to form correct French sentences
- Built-in sentence checker
- Visual streak counter with feedback

### 📘 Conjugations
- Smart verb conjugation table by tense & pronoun
- Integrated search bar
- Dark/light theme support

### 📈 Streak & Progress
- 🔥 Daily streak counter across all game modes
- 📊 Streak graph and max streak stats (Line plot / bar plot)

### 🎧 Daily French Song
- Embedded Spotify player via API
- Random daily French song display
- Playlist creation and control

### 🗃️ Vocabulary Management
- List all saved words
- Search bar and real-time filtering
- Edit and delete individual words

### 👤 Profile Page
- Max streaks per module
- Registered email and account info
- Quick access to all game modes

---

## 🛠 Tech Stack

| Layer       | Stack                  |
|-------------|------------------------|
| Backend     | FastAPI, SQLAlchemy    |
| Frontend    | HTML, Tailwind CSS, JS |
| Database    | PostgreSQL             |
| Auth        | JWT (access token)     |
| Extras      | Spotify Embed API      |

---

## 📁 Project Structure (Simplified)

```
/app
│
├── main.py
├── models.py
├── schemas.py
├── config.py
├── dependencies.py
├── database.py
├── requirements.txt
├── ouicherie.db
├── .env
├── README.md
│
├── /templates
│   ├── layout.html
│   ├── flashcards.html
│   ├── quiz.html
│   ├── ros.html
│   ├── home.html
│   ├── login.html
│   ├── navbar.html
│   ├── register.html
│   ├── profile.html
│   ├── themes.html
│   ├── words.html
│   ├── dashboard.html
│   ├── conjugation.html
│   └── conjugation_table.html
│
├── /static
│   └── /js
│       ├── flashcards_script.js
│       ├── quiz_script.js
│       ├── script.js
│       ├── home_script.js
│       ├── conjugation_script.js
│       ├── dashboard_script.js
│       ├── profile_script.js
│       ├── themes_script.js
│       ├── words_script.js
│       └── ros_script.js
│
├── /routers
│   ├── flashcards.py
│   ├── quiz.py
│   ├── ros.py
│   ├── admin.py
│   ├── auth.py
│   ├── home.py
│   ├── users.py
│   ├── words.py
│   ├── dashboard.py
│   ├── profile.py
│   ├── themes.py
│   ├── songs.py
│   └── conjugations.py
│
├── /utils
│   ├── db_utils.py
│   ├── check_answer_utils.py
│   ├── streak_utils.py
│   ├── theme_utils.py
|   ├── conjugation_utils.py
│   └── auth_utils.py
```

---

## 🧪 Installation (Dev)

```bash
git clone https://github.com/yunuscancengiz/OuiCherie.git
cd OuiCherie

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload
```

---

## ⚙️ Environment Variables

Create a `.env` file with the following:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/yourdb
SECRET_KEY=your_jwt_secret
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

---

## 📦 Deployment

This project is now deployed using a separate private repo (`OuiCherie-Deployment`) that includes `.env`, `.db`, and configuration files.

---

## 📄 License

MIT License © 2025 [Yunus Can Cengiz]

---

🥐 *Made for French learners with ❤️*