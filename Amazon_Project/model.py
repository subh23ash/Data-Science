import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
import openpyxl

file_path = 'subash.xlsx'
data = pd.read_excel(file_path)

X = data[['Actual Price', 'Rating', 'Number of Ratings']]
y = data['Target']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_pred_prob = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_prob)
print("Accuracy:", accuracy)
print("ROC-AUC Score:", roc_auc)

purchase_probabilities = model.predict_proba(X_scaled)[:, 1]
data['Purchase Probability'] = purchase_probabilities*100

output_file_path = 'Updated_Amazonwebscraping_with_probabilities.xlsx'
data.to_excel(output_file_path, index=False)
print(f"Updated Excel file saved as {output_file_path}")
