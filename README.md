# Minimal Pomodoro ⏱️

**Minimal Pomodoro** is a modern, responsive, and minimalist Pomodoro Focus Timer web application built with **Django** and **Vanilla Javascript**. 

Designed as a sleek developer portfolio piece, this application avoids bloated styling frameworks to deliver a premium user experience featuring frosted glass visual elements (glassmorphism), shifting dark-glow radial gradients, synthesized sound chime alerts (using the Web Audio API), desktop notifications, and real-time Chart.js interactive analytics.

---

## ✨ Features

- **🎯 Shifting Dark-Glow Aesthetics**: Deep, ambient radial gradients that shift smoothly to reflect the current mode:
  - **Pomodoro (Focus)**: Crimson Dark Radial Glow
  - **Short Break**: Deep Teal Dark Radial Glow
  - **Long Break**: Steel Blue Dark Radial Glow
- **⏱️ Responsive Timer Controls**: Precise start/pause controls inside a responsive card layout. Tab selectors let you cycle between modes instantly.
- **📝 Inline Task Board**: Create, complete, and delete tasks directly in the workspace. Selecting a task dynamically links it to your active focus session.
- **📊 Focus Reports**: A detailed modal overlay featuring:
  - Numerical aggregates for total focus time, completed cycles, and success rate.
  - Interactive **Chart.js graphs** showing weekly progress and task distributions.
  - A scrollable focus history ledger showing all completed sessions.
- **🔔 Dynamic Sound & Desktop Alerts**:
  - Browser audio synthesis via the **Web Audio API** plays satisfying chime sounds without requiring static audio file downloads.
  - Integrated **Desktop Notifications API** lets you stay updated when working in other browser tabs.
- **⚡ Zero Page Refreshes**: Dynamic AJAX/JSON views sync tasks and focus sessions with the Django SQLite ledger in the background.

---

## 🛠️ Technology Stack

- **Backend**: Python, Django (REST JSON views, ORM migrations, and template rendering)
- **Frontend**: HTML5, Vanilla CSS (Glassmorphism layout), Vanilla ES6+ Javascript
- **Analytics Charts**: Chart.js (loaded via CDN)
- **Database**: SQLite (default ledger database)

---

## 📂 Project Structure

```text
├── config/
│   ├── settings.py      # App configurations & registered modules
│   ├── urls.py          # Root URL mapping
│   └── wsgi.py
├── tracker/
│   ├── migrations/      # Database migrations ledger
│   ├── templates/
│   │   └── tracker/
│   │       └── index.html # Main frontend layout, modern SVGs & JS controller
│   ├── models.py        # Task and PomodoroSession models
│   ├── views.py         # Main templates & REST JSON views
│   ├── urls.py          # App level API routing paths
│   └── tests.py         # Unit tests suite
├── manage.py
├── requirements.txt     # Python dependency configuration
└── .gitignore           # Git ignore patterns
```

---

## 🚀 Setup & Installation Instructions

Follow these steps to run the application locally on your machine:

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/minimal-pomodoro.git
cd minimal-pomodoro
```

### 2. Create and activate a Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run database migrations
```bash
python manage.py migrate
```

### 5. Start the development server
```bash
python manage.py runserver
```

Once running, navigate to **`http://127.0.0.1:8000/`** in your web browser.

---

## 🧪 Running Unit Tests

The project includes unit tests validating the models, endpoint security (CSRF handling), and API calculation logic.

To run the test suite:
```bash
python manage.py test
```
