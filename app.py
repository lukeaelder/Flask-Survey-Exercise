from flask import Flask, request, render_template, redirect, flash, session
app = Flask(__name__)
from surveys import surveys

app.secret_key = '_5dsF#y2L.w43"F4Q8z#4$wdscP98.dwd.c]/'


@app.before_request
def before_request():
    if 'survey_answers' not in session:
            session['survey_answers'] = {}

@app.route('/')
def home_page():
    """Show home page"""
    return render_template('home.html', surveys = surveys)

@app.route('/questions/<question_num>')
def question_page(question_num):
    """Take user to question form"""
    if question_num.isdigit():
        try:
            survey = surveys[request.args.get('s')]
        except:
            flash('Invalid URL, survey name is missing, or incorrect.')
            return redirect('/')

        curr_survey = request.args.get('s')
        survey_answers = session['survey_answers']

        if curr_survey not in survey_answers:
            survey_answers[curr_survey] = []
            session['survey_asnwers'] = survey_answers

        curr_question = len(survey_answers[curr_survey])

        if curr_question == len(survey.questions):
            return redirect(f'/complete?s={curr_survey}')

        if (curr_question != int(question_num)):
            return redirect(f"/questions/{len(survey_answers[curr_survey])}?s={curr_survey}")

        return render_template('question.html', question_num = int(question_num), survey = survey, surveys = surveys)
    else:
        flash('Invalid question number in URL')
        return redirect('/')

@app.route("/answer", methods=["POST"])
def answer_question():
    """Process answer to question"""
    survey_answers = session['survey_answers']
    survey = request.form['s']
    choice = request.form['answer']
    try:
        text_choice = request.form['text-answer']
    except:
        text_choice = None

    curr_question = len(survey_answers[survey])

    if curr_question < len(surveys[survey].questions):
        if text_choice != None:
            survey_answers[survey] = survey_answers.get(survey, []) + [[choice, text_choice]]
        else:
            survey_answers[survey] = survey_answers.get(survey, []) + [choice]
        session['survey_answers'] = survey_answers
        return redirect(f'/questions/{curr_question}?s={survey}')
    else:
        return redirect(f'/complete?s={survey}')

@app.route("/complete")
def complete_page():
    """Show completed survey page"""
    survey = request.args.get('s')
    return render_template('completedsurvey.html', survey = survey)

@app.errorhandler(404)
def page_not_found(e):
    flash('Page was not found, 404 ERROR')
    return redirect('/')