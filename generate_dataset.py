
import pandas as pd
import random

random.seed(42)

rows = []

for i in range(2000):

    # Generate scores from 1 to 10
    pro_quality = random.randint(1, 10)
    pro_relevance = random.randint(1, 10)
    pro_reasoning = random.randint(1, 10)

    con_quality = random.randint(1, 10)
    con_relevance = random.randint(1, 10)
    con_reasoning = random.randint(1, 10)

    # Give different importance to different factors
    pro_score = (
        pro_quality * 0.35
        + pro_relevance * 0.30
        + pro_reasoning * 0.35
    )

    con_score = (
        con_quality * 0.35
        + con_relevance * 0.30
        + con_reasoning * 0.35
    )

    # Add a small amount of randomness for ambiguous cases
    pro_score += random.uniform(-1.5, 1.5)
    con_score += random.uniform(-1.5, 1.5)

    if pro_score > con_score:
        winner = "Pro"
    else:
        winner = "Con"

    rows.append([
        pro_quality,
        pro_relevance,
        pro_reasoning,
        con_quality,
        con_relevance,
        con_reasoning,
        winner
    ])


# Create DataFrame
data = pd.DataFrame(
    rows,
    columns=[
        "Pro Quality",
        "Pro Relevance",
        "Pro Reasoning",
        "Con Quality",
        "Con Relevance",
        "Con Reasoning",
        "Winner"
    ]
)

# Save new dataset
data.to_csv("debate_dataset_v2.csv", index=False)

print("Dataset created successfully!")
print("Rows:", len(data))
print("\nWinner counts:")
print(data["Winner"].value_counts())
