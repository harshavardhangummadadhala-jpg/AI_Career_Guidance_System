import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Demonstration training data.
# Replace/expand this dataset for a real academic project.
data = pd.DataFrame({
    "python": [5,5,4,2,1,4,5,3,4,5,3,2,1,4,5,3,4,2,5,4,5,4,2,1],
    "mathematics": [5,4,5,3,2,3,5,4,5,5,3,2,1,4,5,3,4,2,5,4,5,4,2,1],
    "communication": [2,3,2,5,5,4,2,3,2,3,5,5,4,3,2,5,4,5,2,3,2,3,5,5],
    "design": [1,2,1,5,5,2,1,3,2,1,5,4,5,2,1,5,2,5,1,2,1,2,5,5],
    "security": [4,3,5,2,1,5,4,3,5,4,2,1,2,5,4,2,5,3,5,4,5,4,2,1],
    "ai": [5,5,4,1,1,4,5,3,5,5,2,1,2,4,5,2,5,3,5,4,5,5,1,2],
    "career": [
        "AI/ML Engineer","Data Scientist","AI/ML Engineer","UI/UX Designer",
        "UI/UX Designer","Cybersecurity Analyst","Data Scientist","Software Developer",
        "AI/ML Engineer","Data Scientist","Digital Marketer","Digital Marketer",
        "Digital Marketer","Cybersecurity Analyst","AI/ML Engineer","Digital Marketer",
        "Cybersecurity Analyst","UI/UX Designer","Data Scientist","Software Developer",
        "AI/ML Engineer","Software Developer","UI/UX Designer","Digital Marketer"
    ]
})

X = data.drop("career", axis=1)
y = data["career"]

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)
model.fit(X, y_encoded)

with open("career_model.pkl", "wb") as f:
    pickle.dump((model, encoder), f)

print("SUCCESS: career_model.pkl created.")
