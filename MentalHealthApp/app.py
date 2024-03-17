from flask import Flask, render_template, redirect, session, url_for, request
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
app.secret_key = 'your_secret_key'

'''
questions_with_options = {
    "How are you feeling today?": ["Stressed", "Anxious", "Okay", "Good"],
    "How would you describe your sleep quality recently?": ["Poor", "Fair", "Good", "Excellent"],
    "Have you experienced any changes in appetite or eating habits lately?": ["Yes, increased/decreased appetite", "No change"],
    "Do you find it difficult to concentrate or make decisions?": ["Yes, frequently", "Sometimes", "Rarely", "Never"]
}
'''

# These variables are used to insert to the database
question1_ans = ""
question2_ans = ""
question3_ans = ""
question4_ans = ""

# Home
@app.route("/")
def home():
    return render_template("home.html")

# Question 1 
@app.route("/question1", methods=["GET", "POST"])
def question1():
    global question1_ans

    if request.method == "POST":
        selected_option = request.form.get("option")
        if selected_option:
            session["selected_option"] = selected_option
            question1_ans = selected_option
            return redirect(url_for("question2"))
        else:
            return render_template("question1.html", error="Please select an option")
    
    # Allow user to revisit question1 even if an option is selected
    if session.get("selected_option"):
        return render_template("question1.html", selected_option=session["selected_option"])
    else:
        return render_template("question1.html")

# Question 2
@app.route("/question2", methods=["GET", "POST"])
def question2():
    global question2_ans

    if request.method == "POST":
        selected_option = request.form.get("option")
        if selected_option:
            session["selected_option"] = selected_option
            question2_ans = selected_option
            return redirect(url_for("question3"))
        else:
            return render_template("question2.html", error="Please select an option")
    
    # Allow user to revisit question1 even if an option is selected
    if session.get("selected_option"):
        return render_template("question2.html", selected_option=session["selected_option"])
    else:
        return render_template("question2.html")

# Question 3
@app.route("/question3", methods=["GET", "POST"])
def question3():
    global question3_ans

    if request.method == "POST":
        selected_option = request.form.get("option")
        if selected_option:
            session["selected_option"] = selected_option
            question3_ans = selected_option
            return redirect(url_for("question4"))
        else:
            return render_template("question3.html", error="Please select an option")
    
    # Allow user to revisit question1 even if an option is selected
    if session.get("selected_option"):
        return render_template("question3.html", selected_option=session["selected_option"])
    else:
        return render_template("question3.html")

# Question 4
@app.route("/question4", methods=["GET", "POST"])
def question4():
    global question4_ans

    if request.method == "POST":
        selected_option = request.form.get("option")
        if selected_option:
            session["selected_option"] = selected_option
            question4_ans = selected_option
            return redirect(url_for("completion"))
        else:
            return render_template("question4.html", error="Please select an option")
    
    # Allow user to revisit question1 even if an option is selected
    if session.get("selected_option"):
        return render_template("question4.html", selected_option=session["selected_option"])
    else:
        return render_template("question4.html")

@app.route("/completion")
def completion():
    if all([question1_ans, question2_ans, question3_ans, question4_ans]):
        
        df = pd.DataFrame([[question1_ans, question2_ans, question3_ans, question4_ans]], columns = ['question1', 'question2', 'question3', 'question4'])
        mental_health = training_model(df)
        
        if mental_health == 'Yes':
            help = "Yes"
        else:
            help = "No"

        # Connect to database and set cursor
        conn = sqlite3.connect("database.db")
        db_cursor = conn.cursor()

        # Query
        query = """INSERT INTO answers (question1, question2, question3, question4) VALUES (?,?,?,?)"""

        # Combine the answers
        all_answers = (question1_ans, question2_ans, question3_ans, question4_ans)

        # Execute the query
        db_cursor.execute(query, all_answers)

        # Commit and close connection
        conn.commit()
        conn.close()

        return render_template("completion.html", help=help)
    else:
        return redirect(url_for("home"))

@app.route("/statistics")
def statistics():
    # Connect to database and set cursor
    conn = sqlite3.connect("database.db")
    db_cursor = conn.cursor()

    # Execute SQL queries to get the count of each item in each column
    query1 = "SELECT question1, COUNT(*) FROM answers GROUP BY question1"
    query2 = "SELECT question2, COUNT(*) FROM answers GROUP BY question2"
    query3 = "SELECT question3, COUNT(*) FROM answers GROUP BY question3"
    query4 = "SELECT question4, COUNT(*) FROM answers GROUP BY question4"

    # Execute the query and fetch the results
    db_cursor.execute(query1)
    answers_count1 = db_cursor.fetchall()
    db_cursor.execute(query2)
    answers_count2 = db_cursor.fetchall()
    db_cursor.execute(query3)
    answers_count3 = db_cursor.fetchall()
    db_cursor.execute(query4)
    answers_count4 = db_cursor.fetchall()

    # Close connection
    conn.close()

    # Variables for each answer dictionary
    answers1_dict = {}
    answers2_dict = {}
    answers3_dict = {}
    answers4_dict = {}

    # Populate dictionary with they key(answer) and the value(count)
    for row in answers_count1:
        answers1_dict[row[0]] = row[1]

    for row in answers_count2:
        answers2_dict[row[0]] = row[1]

    for row in answers_count3:
        answers3_dict[row[0]] = row[1]

    for row in answers_count4:
        answers4_dict[row[0]] = row[1]

    question1_labels = str(list(answers1_dict.keys()))
    question1_labels = question1_labels[1:-1]
    question1_labels = question1_labels.replace("'", "")
    question1_counts = str(list(answers1_dict.values()))
    question1_counts = question1_counts[1:-1]
    question1_counts = question1_counts.replace("'", "")

    question2_labels = str(list(answers2_dict.keys()))
    question2_labels = question2_labels[1:-1]
    question2_labels = question2_labels.replace("'", "")
    question2_counts = str(list(answers2_dict.values()))
    question2_counts = question2_counts[1:-1]
    question2_counts = question2_counts.replace("'", "")

    question3_labels = str(list(answers3_dict.keys()))
    question3_labels = question3_labels[1:-1]
    question3_labels = question3_labels.replace("'", "")
    question3_counts = str(list(answers3_dict.values()))
    question3_counts = question3_counts[1:-1]
    question3_counts = question3_counts.replace("'", "")

    question4_labels = str(list(answers4_dict.keys()))
    question4_labels = question4_labels[1:-1]
    question4_labels = question4_labels.replace("'", "")
    question4_counts = str(list(answers4_dict.values()))
    question4_counts = question4_counts[1:-1]
    question4_counts = question4_counts.replace("'", "")
   
    return render_template("statistics.html", question1_labels=question1_labels, 
                                                question1_counts=question1_counts,
                                                question2_labels=question2_labels,
                                                question2_counts=question2_counts,
                                                question3_labels=question3_labels,
                                                question3_counts=question3_counts,
                                                question4_labels=question4_labels,
                                                question4_counts=question4_counts)

def training_model(df):
    # Connect to the SQLite sample_database.db
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

    df_encoded = df.copy()
    for col, encoder in encoder_dict.items():
        df_encoded[col] = encoder.transform(df[col])

    return model.predict(df_encoded)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)