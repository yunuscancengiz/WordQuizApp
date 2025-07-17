# 🇫🇷 OuiChérie – Your Fun & Smart French Learning App

**OuiChérie** is an interactive, gamified French learning platform built with FastAPI and vanilla JavaScript. Designed to help users master vocabulary, sentence structure, and verb conjugations while keeping track of their daily progress through streaks and visualizations.

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
- 📊 Streak graph and max streak stats (Line plot / bar plot coming soon)

### 🎧 Daily French Song *(Coming Soon)*
- Embedded Spotify player via API
- Random daily French song display
- Playlist creation and control

### 🗃️ Vocabulary Management *(Coming Soon)*
- List all saved words
- Search bar and real-time filtering
- Edit and delete individual words

### 👤 Profile Page *(To be Updated)*
- Show max streaks per module
- Display registered email and account info
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
│
├── /templates       # Jinja2 HTML templates
│   ├── layout.html
│   ├── flashcards.html
│   ├── quiz.html
│   ├── ros.html
│   └── conjugation_table.html
│
├── /static
│   └── /js
│       ├── flashcards_script.js
│       ├── quiz_script.js
│       └── ros_script.js
│
├── /routers
│   ├── flashcards.py
│   ├── quiz.py
│   ├── ros.py
│   └── conjugations.py
│
├── /utils
│   ├── db_utils.py
│   └── auth_utils.py
│
└── /dependencies
    └── db_dependency.py
```

---

## 🧪 Installation (Dev)

```bash
git clone https://github.com/yourusername/ouicherie.git
cd ouicherie

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

Create a `.env` file with the following (or manage via `config.py`):

```env
DATABASE_URL=postgresql://user:password@localhost:5432/yourdb
SECRET_KEY=your_jwt_secret
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

---

## 🔮 Roadmap

- [x] Flashcards with example sentences
- [x] Quiz mode with multiple choices
- [x] Sentence construction game (ROS)
- [x] Conjugation table
- [x] Streak system
- [ ] Spotify integration for daily songs & playlists
- [ ] Word list management with search, edit, delete
- [ ] Enhanced user profile
- [ ] Admin panel (future dev use)

---

## 📄 License

MIT License © 2025 [Your Name or Team Name]

---

🥐 *Made for French learners.*
