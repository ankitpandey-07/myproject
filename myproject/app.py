import json
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for session management and flash messages

USER_DATA_FILE = 'users.json'

# Load user data from JSON file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save user data to JSON file
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file, indent=4)

# Register User
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        users = load_user_data()
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        if username in users:
            flash('Username already exists. Try a different one.', 'error')
            return redirect(url_for('register_user'))

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        users[username] = hashed_password.decode('utf-8')
        save_user_data(users)
        flash('Registration successful!', 'success')
        return redirect(url_for('login_user'))

    return render_template('register.html')

# Login User
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        users = load_user_data()
        username = request.form['username']
        password = request.form['password']

        # Check if username exists and validate password
        if username in users and bcrypt.checkpw(password.encode(), users[username].encode()):
            return redirect(url_for('play_game'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

# MCQ Game
@app.route('/game', methods=['GET', 'POST'])
def play_game():
    questions = [
        {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin", "Madrid"], "correct_option": 1},
        {"question": "What is 5 + 7?", "options": ["10", "11", "12", "13"], "correct_option": 3},
        {"question": "Who wrote 'Hamlet'?", "options": ["Shakespeare", "Dickens", "Hemingway", "Tolkien"], "correct_option": 1},
        {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "correct_option": 2},
        {"question": "What is the square root of 64?", "options": ["6", "7", "8", "9"], "correct_option": 3}
    ]
    
    score = 0
    if request.method == 'POST':
        for idx, question in enumerate(questions):
            answer = int(request.form.get(f'question_{idx}'))
            if answer == question['correct_option']:
                score += 1

        return render_template('game.html', score=score, total=len(questions))

    return render_template('game.html', questions=questions)

# Home Route
@app.route('/')
def home():
    return redirect(url_for('login_user'))

if __name__ == '__main__':
    app.run(debug=True)
