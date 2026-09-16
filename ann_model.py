import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train_ann():
    # Load dataset from CSV
    data = pd.read_csv("debate_dataset_v2.csv")

    # Input features
    X = data[
        [
            "Pro Quality",
            "Pro Relevance",
            "Pro Reasoning",
            "Con Quality",
            "Con Relevance",
            "Con Reasoning"
        ]
    ]

    # Expected output
    y = data["Winner"]

    # Split dataset into training and testing data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Create ANN model
    model = MLPClassifier(
        hidden_layer_sizes=(10,),
        max_iter=5000,
        random_state=42
    )

    # Train ANN
    model.fit(X_train, y_train)

    # Test ANN on unseen data
    predictions = model.predict(X_test)

    
    train_predictions = model.predict(X_train)

    train_accuracy = accuracy_score(y_train, train_predictions)
    test_accuracy = accuracy_score(y_test, predictions)

    print("Training Accuracy:", train_accuracy)
    print("Testing Accuracy:", test_accuracy)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, predictions)

    print("ANN Accuracy:", accuracy)

    return model


def predict_winner(model, scores):
    prediction = model.predict([scores])[0]
    probabilities = model.predict_proba([scores])[0]

    # Find which probability belongs to Pro and Con
    classes = model.classes_

    pro_probability = probabilities[list(classes).index("Pro")]
    con_probability = probabilities[list(classes).index("Con")]

    return {
        "winner": prediction,
        "pro_probability": pro_probability,
        "con_probability": con_probability
    }

