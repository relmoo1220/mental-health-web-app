from flask import Flask, render_template, redirect, session, url_for, request
import sqlite3

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

        return render_template("completion.html")
    else:
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()