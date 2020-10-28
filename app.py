from flask import Flask, request, render_template, redirect, flash
app = Flask(__name__)
from surveys import surveys

survey_answers = {}

@app.route('/')
def home_page():
    return render_template('home.html', surveys = surveys)

@app.route('/questions/<question_num>')
def question_page(question_num):
    if question_num.isdigit():
        try:
            survey = surveys[request.args.get('s')]
        except:
            return redirect('/')
        curr_survey = request.args.get('s')
        if curr_survey in survey_answers:
            curr_question = len(survey_answers[curr_survey])
            if curr_question == len(survey.questions):
                return redirect('/complete')
            if (curr_question != int(question_num)):
                return redirect(f"/questions/{len(survey_answers[curr_survey])}?s={curr_survey}")
        if 0 <= int(question_num) < len(survey.questions):
            return render_template('question.html', question_num = int(question_num), survey = survey, surveys = surveys)
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route("/answer", methods=["POST"])
def answer_question():
    survey = request.form['s']
    choice = request.form['answer']
    survey_answers[survey] = survey_answers.get(survey, []) + [choice]
    curr_question = len(survey_answers[survey])
    if curr_question < len(surveys[survey].questions):
        return redirect(f'/questions/{curr_question}?s={survey}')
    else:
        return redirect('/complete')

@app.route("/complete")
def complete_page():
    return render_template('completedsurvey.html')