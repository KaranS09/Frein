import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import ollama
import time

# -----------------------------
# 1. Load dataset
# -----------------------------

df = pd.read_csv("events.csv")

# clean column names
df.columns = df.columns.str.strip()

# -----------------------------
# 2. Combine text columns
# -----------------------------

df["combined_text"] = (
    df["Name of the event"].astype(str) + " " +
    df["Event description"].astype(str) + " " +
    df["Type of event"].astype(str) + " " +
    df["Genre"].astype(str)
)

texts = df["combined_text"].tolist()

# -----------------------------
# 3. Load embedding model
# -----------------------------

print("Loading embedding model...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = embedding_model.encode(texts)

embeddings = np.array(embeddings).astype("float32")

# -----------------------------
# 4. Build FAISS index
# -----------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print("Vector index built with", len(embeddings), "events")

# -----------------------------
# 5. Prediction function
# -----------------------------

def predict_group_size(event_text, top_k=5):

    query_embedding = embedding_model.encode([event_text]).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    similar_events = df.iloc[indices[0]]

    context = ""

    for _, row in similar_events.iterrows():
        context += f"""
Event: {row['Name of the event']}
Description: {row['Event description']}
Type: {row['Type of event']}
Genre: {row['Genre']}
"""

    prompt = f"""
You are estimating the ideal group size for attending events.

General patterns:
- Workshops → 1-3 people
- Networking → 2-4
- Comedy shows → 3-4
- Concerts → 4-8
- Festivals → 6+

Event to evaluate:
{event_text}

Here are similar events:

{context}

Predict the ideal group size.

Return ONLY a number.
"""

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

# -----------------------------
# 6. Predict for all events
# -----------------------------

predictions = []

for i, row in df.iterrows():

    event_text = row["combined_text"]

    print(f"Processing event {i+1}/{len(df)}")

    prediction = predict_group_size(event_text)

    predictions.append(prediction)

    time.sleep(0.5)  # prevents overloading the model

# -----------------------------
# 7. Add column to dataframe
# -----------------------------

df["Predicted group size"] = predictions

# -----------------------------
# 8. Save updated CSV
# -----------------------------

df.to_csv("events_with_group_size.csv", index=False)

print("\nSaved predictions to events_with_group_size.csv")