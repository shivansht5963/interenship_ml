import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

# Load and preprocess dataset
df = pd.read_csv("student_dataset.csv")
df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
df['Result'] = df['Result'].map({'Pass': 1, 'Fail': 0})
X, y = df.drop('Result', axis=1), df['Result']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train SVM model
model = SVC(kernel='linear', probability=True, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=["Fail", "Pass"], zero_division=0))

# Confusion matrix
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, display_labels=["Fail", "Pass"])
plt.title("Confusion Matrix")
plt.show()

# Probability plot
sns.lineplot(x=range(len(y_proba)), y=y_proba, marker='o')
plt.title("Predicted Probabilities (Pass)")
plt.xlabel("Test Sample Index")
plt.ylabel("Probability")
plt.grid(True)
plt.show()
