# 🥗 Diet Plan Website

A simple, beginner-friendly Flask web app that saves user diet preferences into a SQLite database.
Runs instantly — locally **or** on Replit — with zero configuration needed.

---

## 📁 Project Structure

```
diet_final/
│
├── app.py            ← The ONLY file you need — backend + frontend combined
├── requirements.txt  ← Just one dependency: Flask
├── README.md         ← This file
└── diet.db           ← Auto-created on first run (don't create manually)
```

> ✅ There is no separate `index.html` needed.
> The HTML page is embedded directly inside `app.py` using `render_template_string`.
> This keeps the whole project in **one simple file**.

---

## ✅ Frontend ↔ Backend Match Checklist

| Item | Status |
|---|---|
| Form `action="/save"` matches `@app.route('/save')` | ✅ |
| Form `method="POST"` matches `methods=['POST']` | ✅ |
| Input `name="name"` matches `request.form.get('name')` | ✅ |
| Input `name="age"` matches `request.form.get('age')` | ✅ |
| Select `name="diet_type"` matches `request.form.get('diet_type')` | ✅ |
| DB columns match form fields | ✅ |
| `{% if message %}` rendered via `render_template_string` | ✅ |
| `/save` returns the page + message (not plain text) | ✅ |

---

## 🚀 How to Run

### Step 1 — Install Flask
```bash
pip install -r requirements.txt
```

### Step 2 — Start the app
```bash
python app.py
```

### Step 3 — Open in browser
```
http://localhost:5000
```

---

## 🌐 Running on Replit?

Works out of the box! Just:
1. Upload `app.py` and `requirements.txt` to your Replit project
2. Click the **Run** button
3. Open the Replit web preview panel

The `diet.db` file will be created automatically — no setup needed.

---

## 🗄️ What Gets Saved to the Database?

Every form submission saves one row to the `user_diets` table:

| Column | Type | Example |
|---|---|---|
| id | Auto number | 1, 2, 3... |
| name | Text | Alex |
| age | Number | 22 |
| diet_type | Text | Weight Loss |

---

## 💡 How It Works (Beginner Explanation)

1. You visit `http://localhost:5000` → Flask runs the `home()` function → shows the form
2. You fill in the form and click **Save My Plan**
3. The browser sends your data to `/save` using POST
4. Flask reads the data, saves it to `diet.db`, then reloads the page with a ✅ success message
