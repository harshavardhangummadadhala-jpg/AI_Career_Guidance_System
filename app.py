from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import db, User, Assessment
import pickle
import numpy as np

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///career.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

try:
    with open("career_model.pkl", "rb") as f:
        model, encoder = pickle.load(f)
except FileNotFoundError:
    raise SystemExit("career_model.pkl not found. Run: python model.py")

CAREER_INFO = {
    "AI/ML Engineer": {
        "description": "Build intelligent systems using machine learning, deep learning and AI.",
        "skills": ["Python", "Statistics", "Machine Learning", "Deep Learning", "TensorFlow", "SQL"],
        "roadmap": ["Learn Python", "Learn Statistics", "Learn SQL", "Learn Machine Learning", "Build ML projects", "Learn Deep Learning", "Build an AI portfolio"],
        "courses": ["Machine Learning Specialization", "Deep Learning fundamentals", "Python for Data Science"]
    },
    "Data Scientist": {
        "description": "Turn data into useful insights and predictive models.",
        "skills": ["Python", "Statistics", "SQL", "Pandas", "Data Visualization", "Machine Learning"],
        "roadmap": ["Learn Python", "Learn SQL", "Learn Statistics", "Learn Pandas", "Practice visualization", "Learn Machine Learning", "Build data projects"],
        "courses": ["Python Data Analysis", "Statistics for Data Science", "Applied Machine Learning"]
    },
    "Cybersecurity Analyst": {
        "description": "Protect systems, networks and data from security threats.",
        "skills": ["Networking", "Linux", "Python", "Cybersecurity", "Ethical Hacking", "Security Tools"],
        "roadmap": ["Learn networking", "Learn Linux", "Learn cybersecurity basics", "Practice labs", "Learn security tools", "Build security projects"],
        "courses": ["Networking fundamentals", "Cybersecurity fundamentals", "Ethical hacking labs"]
    },
    "UI/UX Designer": {
        "description": "Design useful, accessible and attractive digital experiences.",
        "skills": ["Figma", "UI Design", "UX Research", "Wireframing", "Prototyping", "Visual Design"],
        "roadmap": ["Learn design principles", "Learn Figma", "Practice wireframes", "Learn UX research", "Create prototypes", "Build a portfolio"],
        "courses": ["Figma UI Design", "UX Research basics", "Design portfolio workshop"]
    },
    "Software Developer": {
        "description": "Design, build, test and maintain software applications.",
        "skills": ["Programming", "Data Structures", "Algorithms", "Git", "Databases", "Problem Solving"],
        "roadmap": ["Learn programming", "Learn data structures", "Learn algorithms", "Learn Git", "Build projects", "Practice coding interviews"],
        "courses": ["Programming fundamentals", "Data Structures and Algorithms", "Git and GitHub"]
    },
    "Digital Marketer": {
        "description": "Grow products and brands through digital channels and analytics.",
        "skills": ["SEO", "Social Media", "Content Marketing", "Analytics", "Advertising", "Copywriting"],
        "roadmap": ["Learn digital marketing", "Learn SEO", "Learn social media", "Learn analytics", "Run small campaigns", "Build a marketing portfolio"],
        "courses": ["SEO fundamentals", "Digital marketing basics", "Analytics and reporting"]
    }
}

def login_required():
    return "user_id" in session

@app.route("/")
def home():
    return redirect(url_for("dashboard" if login_required() else "login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if len(password) < 6:
            flash("Password must contain at least 6 characters.")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered.")
            return redirect(url_for("register"))

        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("login"))

    assessments = Assessment.query.filter_by(
        user_id=session["user_id"]
    ).order_by(Assessment.id.desc()).all()

    return render_template(
        "dashboard.html",
        assessments=assessments
    )

@app.route("/assessment", methods=["GET", "POST"])
def assessment():
    if not login_required():
        return redirect(url_for("login"))

    if request.method == "POST":
        fields = ["python", "mathematics", "communication", "design", "security", "ai"]

        try:
            features = [int(request.form[field]) for field in fields]
        except (KeyError, ValueError):
            flash("Please answer every question.")
            return redirect(url_for("assessment"))

        if any(value < 1 or value > 5 for value in features):
            flash("Each rating must be between 1 and 5.")
            return redirect(url_for("assessment"))

        X = np.array(features).reshape(1, -1)
        prediction = model.predict(X)
        career = encoder.inverse_transform(prediction)[0]

        probabilities = model.predict_proba(X)[0]
        top_indexes = np.argsort(probabilities)[::-1][:3]

        top_careers = [
            {
                "career": encoder.inverse_transform([i])[0],
                "probability": round(float(probabilities[i]) * 100, 1)
            }
            for i in top_indexes
        ]

        score = round(float(max(probabilities)) * 100, 1)
        info = CAREER_INFO.get(career, {})

        record = Assessment(
            user_id=session["user_id"],
            python=features[0],
            mathematics=features[1],
            communication=features[2],
            design=features[3],
            security=features[4],
            ai=features[5],
            predicted_career=career,
            score=score
        )
        db.session.add(record)
        db.session.commit()

        return render_template(
            "result.html",
            career=career,
            score=score,
            top_careers=top_careers,
            info=info,
            features=dict(zip(fields, features))
        )

    return render_template("assessment.html")

@app.route("/profile")
def profile():
    if not login_required():
        return redirect(url_for("login"))
    user = User.query.get(session["user_id"])
    return render_template("profile.html", user=user)

@app.route("/assessments")
def assessments():
    if not login_required():
        return redirect(url_for("login"))
    rows = Assessment.query.filter_by(
        user_id=session["user_id"]
    ).order_by(Assessment.id.desc()).all()
    return render_template("assessments.html", assessments=rows)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
