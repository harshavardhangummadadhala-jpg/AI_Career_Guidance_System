# AI-Based Career Guidance System

A complete final-year project starter built with Flask, SQLite, Scikit-learn and a responsive web UI.

## Features
- Student registration and login
- Password hashing
- Career assessment
- ML-based career prediction
- Top 3 career recommendations
- Match score
- Required skills
- Personalized learning roadmap
- Assessment history
- Dashboard
- SQLite database

## Requirements
- Python 3.10+
- VS Code (recommended)

## Windows Setup

Open Command Prompt inside this project folder.

1. Create virtual environment:
   python -m venv venv

2. Activate:
   venv\Scripts\activate

3. Install packages:
   pip install -r requirements.txt

4. Train the model:
   python model.py

5. Start the app:
   python app.py

6. Open:
   http://127.0.0.1:5000

## First Demo
1. Click Register
2. Create an account
3. Login
4. Click Take Assessment
5. Enter ratings from 1 to 5
6. Click Analyze My Career
7. View recommendation, top careers, skills and roadmap

## Important
The included ML dataset is a small demonstration dataset. For an academic final submission, replace it with a larger, real and properly licensed career dataset and evaluate the model using train/test split and metrics.
