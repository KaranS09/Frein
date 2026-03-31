import pandas as pd
import numpy as np
import re
import joblib

from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report

# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("LLM/events_with_group_size.csv")
df.columns = df.columns.str.strip()

# -----------------------------
# 2. Clean labels
# -----------------------------
def extract_number(text):
    if pd.isna(text):
        return None
    match = re.search(r'\d+', str(text))
    return int(match.group()) if match else None

df["Predicted group size"] = df["Predicted group size"].apply(extract_number)

df = df.dropna(subset=["Predicted group size"])
df["Predicted group size"] = df["Predicted group size"].astype(int)
df = df[df["Predicted group size"].between(1, 10)]

# -----------------------------
# 3. Convert to classification labels
# -----------------------------
def to_class(x):
    if x <= 2:
        return 0  # small
    elif x <= 4:
        return 1  # medium
    else:
        return 2  # large

df["label"] = df["Predicted group size"].apply(to_class)

# -----------------------------
# 4. Text features
# -----------------------------
df["combined_text"] = (
    df["Name of the event"].astype(str) + " " +
    df["Event description"].astype(str) + " " +
    df["Type of event"].astype(str) + " " +
    df["Genre"].astype(str)
)

# -----------------------------
# 5. Train-test split
# -----------------------------
train_df, test_df = train_test_split(
    df, test_size=0.2, random_state=42
)

train_df.to_csv("train_events.csv", index=False)
test_df.to_csv("test_events.csv", index=False)

print(f"Train size: {len(train_df)}")
print(f"Test size: {len(test_df)}")

# -----------------------------
# 6. Embeddings
# -----------------------------
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Encoding train data...")
X_train = embedding_model.encode(
    train_df["combined_text"].tolist(),
    show_progress_bar=True
)

print("Encoding test data...")
X_test = embedding_model.encode(
    test_df["combined_text"].tolist(),
    show_progress_bar=True
)

y_train = train_df["label"].values
y_test = test_df["label"].values

# -----------------------------
# 7. Train model
# -----------------------------
print("Training classifier...")
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# -----------------------------
# 8. Evaluation
# -----------------------------
y_pred = model.predict(X_test)

print("\n--- Evaluation ---")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred, average="weighted"))

print("\nDetailed Report:\n")
print(classification_report(y_test, y_pred))

# -----------------------------
# 9. Debug predictions
# -----------------------------
print("\nSample Predictions:\n")

label_map = {0: "small", 1: "medium", 2: "large"}

for i in range(min(10, len(test_df))):
    print("Event:", test_df.iloc[i]["Name of the event"])
    print("Actual:", label_map[y_test[i]])
    print("Predicted:", label_map[y_pred[i]])
    print("-" * 50)

# -----------------------------
# 10. Save model
# -----------------------------
joblib.dump(model, "group_size_classifier.pkl")
joblib.dump(embedding_model, "embedding_model.pkl")

print("Models saved!")

# -----------------------------
# 11. Inference function
# -----------------------------
def predict_group_size(name, description, type_, genre):
    text = f"{name} {description} {type_} {genre}"
    emb = embedding_model.encode([text])
    
    pred = model.predict(emb)[0]
    
    label_map = {0: "small (1-2)", 1: "medium (3-4)", 2: "large (5+)"}
    return label_map[pred]

# -----------------------------
# 12. Test inference
# -----------------------------
print("\nTest prediction:")
print(predict_group_size(
    "Live Music Concert",
    "Crowded outdoor concert with food and drinks",
    "Concert",
    "Music"
))