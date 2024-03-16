import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Connect to the SQLite database
conn = sqlite3.connect('sample_database.db')

# Query data from the database
query = 'SELECT question1, question2, question3, question4, help FROM answers'
data = pd.read_sql(query, conn)

# Close the database connection
conn.close()

# Drop rows with missing values
data.dropna(inplace=True)

encoder_dict = {}
for col in ['question1', 'question2', 'question3', 'question4']:
    encoder = LabelEncoder()
    data[col] = encoder.fit_transform(data[col])
    encoder_dict[col] = encoder

X = data.drop(columns = 'help')
Y = data['help']

# 30% of data for testing and 70% of data for training
# Helps to prevent overfitting, where the model learns to memorize the trainig data instead of capturing underlying patterns
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 21)

model = LogisticRegression(random_state = 0).fit(X_train, Y_train)

test_data = ['Anxious', 'Fair', 'No changes', 'Sometimes']
df = pd.DataFrame([test_data], columns=['question1', 'question2', 'question3', 'question4'])

df_encoded = df.copy()
for col, encoder in encoder_dict.items():
    df_encoded[col] = encoder.transform(df[col])

print(df_encoded)
print(model.predict(df_encoded))
