from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# ─────────────────────────────────────────────
# STEP 1 — DATABASE SETUP
# Creates diet.db and the table automatically
# ─────────────────────────────────────────────
def init_db():
    connection = sqlite3.connect('diet.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_diets (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT,
            age       INTEGER,
            diet_type TEXT
        )
    ''')
    connection.commit()
    connection.close()

init_db()  # Run once when the app starts

# ─────────────────────────────────────────────
# The full vibrant HTML page stored as a string
# Keeping it here means the whole app is 1 file
# ─────────────────────────────────────────────
HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>🥗 My Diet Planner</title>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap" rel="stylesheet"/>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }

    /* Animated rainbow gradient background */
    body {
      font-family: "Nunito", sans-serif;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #f83b6e, #fc8c4a, #ffd93d, #6bcb77, #4d96ff);
      background-size: 400% 400%;
      animation: bgShift 8s ease infinite;
      padding: 20px;
    }
    @keyframes bgShift {
      0%   { background-position: 0% 50%; }
      50%  { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    /* White card in the centre */
    .card {
      background: white;
      border-radius: 24px;
      padding: 40px 36px;
      width: 100%;
      max-width: 460px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.2);
      animation: popIn 0.5s ease;
    }
    @keyframes popIn {
      from { transform: scale(0.85); opacity: 0; }
      to   { transform: scale(1);    opacity: 1; }
    }

    /* Rainbow gradient title */
    h1 {
      text-align: center;
      font-size: 2rem;
      font-weight: 900;
      background: linear-gradient(90deg, #f83b6e, #fc8c4a, #ffd93d, #6bcb77, #4d96ff);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 8px;
    }
    .subtitle {
      text-align: center;
      color: #888;
      font-size: 0.95rem;
      margin-bottom: 28px;
    }

    /* Each label + input group */
    .field { margin-bottom: 18px; }
    label {
      display: block;
      font-weight: 700;
      color: #333;
      margin-bottom: 6px;
      font-size: 0.95rem;
    }
    input, select {
      width: 100%;
      padding: 12px 16px;
      border: 2px solid #e0e0e0;
      border-radius: 12px;
      font-size: 1rem;
      font-family: "Nunito", sans-serif;
      transition: border-color 0.2s;
      outline: none;
      color: #333;
    }
    input:focus, select:focus { border-color: #4d96ff; }

    /* Submit button */
    button {
      width: 100%;
      padding: 14px;
      margin-top: 10px;
      background: linear-gradient(90deg, #f83b6e, #fc8c4a);
      color: white;
      font-size: 1.1rem;
      font-weight: 900;
      font-family: "Nunito", sans-serif;
      border: none;
      border-radius: 14px;
      cursor: pointer;
      transition: transform 0.15s, box-shadow 0.15s;
    }
    button:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(248,59,110,0.4);
    }

    /* Green success message */
    .message {
      margin-top: 20px;
      background: #e6f9ee;
      border: 2px solid #6bcb77;
      color: #2d7a3a;
      border-radius: 12px;
      padding: 14px 18px;
      text-align: center;
      font-weight: 700;
      font-size: 1rem;
      animation: fadeIn 0.4s ease;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(8px); }
      to   { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>🥗 Diet Planner</h1>
    <p class="subtitle">Tell us about yourself and we'll save your plan!</p>

    <!-- Form posts to /save using POST -->
    <form action="/save" method="POST">

      <div class="field">
        <label for="name">👤 Your Name</label>
        <input type="text" id="name" name="name" placeholder="e.g. Alex" required/>
      </div>

      <div class="field">
        <label for="age">🎂 Your Age</label>
        <input type="number" id="age" name="age" placeholder="e.g. 22" min="1" max="120" required/>
      </div>

      <div class="field">
        <label for="diet_type">🥑 Diet Goal</label>
        <select id="diet_type" name="diet_type" required>
          <option value="" disabled selected>-- Choose your goal --</option>
          <option value="Weight Loss">⚖️ Weight Loss</option>
          <option value="Muscle Gain">💪 Muscle Gain</option>
          <option value="Healthy Maintenance">🌿 Healthy Maintenance</option>
        </select>
      </div>

      <button type="submit">Save My Plan 🚀</button>
    </form>

    <!-- This block only appears after a successful save -->
    {% if message %}
      <div class="message">✅ {{ message }}</div>
    {% endif %}
  </div>
</body>
</html>
'''

# ─────────────────────────────────────────────
# STEP 2 — ROUTES
# ─────────────────────────────────────────────

# Show the empty form on first visit
@app.route('/')
def home():
    return render_template_string(HTML_PAGE, message=None)

# Handle the form submit
@app.route('/save', methods=['POST'])
def save():
    # Read form values
    user_name = request.form.get('name')
    user_age  = request.form.get('age')
    user_diet = request.form.get('diet_type')

    # Save to database
    connection = sqlite3.connect('diet.db')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO user_diets (name, age, diet_type) VALUES (?, ?, ?)",
        (user_name, user_age, user_diet)
    )
    connection.commit()
    connection.close()

    # Re-render the same page with the success message shown
    return render_template_string(HTML_PAGE, message="Diet preference saved successfully")

# ─────────────────────────────────────────────
# STEP 3 — RUN THE SERVER
# ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
