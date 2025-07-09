# save_model.py
import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# Sample dataset
data = pd.DataFrame({
    'hours': [1, 2, 3, 4, 5, 6, 7],
    'attendance': [30, 40, 50, 60, 70, 80, 90],
    'passed': [0, 0, 0, 1, 1, 1, 1]
})

X = data[['hours', 'attendance']]
y = data['passed']

model = LogisticRegression()
model.fit(X, y)

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
