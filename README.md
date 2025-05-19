# IngrecipeAI

IngrecipeAI is a modern, youth-focused web app that helps you discover personalized, healthy recipes based on your ingredients, health goals, and lifestyle. Powered by Flask and an external AI API, IngrecipeAI is designed for anyone who wants to eat better, get fit, or simply try something new—no database or account required!

---

## 🚀 Features
- **Personalized Recipes:** Get suggestions based on your BMI, dietary preference, fitness goal, cuisine, allergies, and activity level.
- **Modern, Responsive UI:** Beautiful, mobile-friendly design with emoji hints and a fun, friendly vibe.
- **Healthy Tip of the Day:** Get a new wellness tip every time you use the app.
- **No Database Needed:** All logic is handled in Python and via API—no setup headaches.
- **Fast & Lightweight:** Runs locally or on any cloud platform that supports Flask.

---

## 🛠️ Tech Stack
- **Backend:** Python 3, Flask, python-dotenv, requests
- **Frontend:** HTML5, CSS3 (custom + Bootstrap), Google Fonts, Emoji
- **API:** External AI-powered recipe API (see `.env` setup)

---

## 📦 Project Structure
```
IngrecipeAI/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── .env                  # API key (not committed)
├── static/               # CSS, images, etc.
├── templates/            # HTML templates
├── README.md             # This file
└── ...
```

---

## ⚡ Getting Started
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd IngrecipeAI
   ```
2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up your API key:**
   - Create a `.env` file in the root directory.
   - Add your API key:
     ```
     API_KEY=your_api_key_here
     ```
5. **Run the app:**
   ```bash
   python app.py
   ```
6. **Open your browser:**
   - Go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🤝 Contributing
Pull requests and suggestions are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 🆘 Support
If you have questions or need help, open an issue or contact the maintainer.

---

## 📄 License
MIT

&copy; 2025 IngrecipeAI. All rights reserved. 