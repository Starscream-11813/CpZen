# from flask.wrappers import Request
# from flask_migrate import current
# from requests.sessions import session
# from werkzeug.datastructures import _CacheControl
from app.profile_stats.spoj_unsolved import SPOJUnsolvedProblems
from app.profile_stats.uva_unsolved import UvaUnsolvedProblems
from app.profile_stats.codeforces_unsolved import CFUnsolvedProblems
from flask_wtf import form
from app import app, db, bcrypt, mail
from flask import render_template, url_for, flash, redirect, request
from app.forms import SubmissionForm, LoginForm, RegistrationForm, ProfileForm, RequestResetForm, ResetPasswordForm, AlgorithmForm
from config import Config
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, SaveCode, tempCode, Algorithm
from datetime import datetime
from app.scrapers.codechef import CodeChef
from app.scrapers.codeforces import CodeForces
from app.profile_stats.codeforces_stat import CodeforcesScrapper
from app.profile_stats.uva_stat import UvaScrapper
from app.profile_stats.codechef_stat import CodeChefScrapper
from app.profile_stats.spoj_stat import SpojScrapper
from app.profile_stats.atcoder_stat import AtCoderScrapper
from app.profile_stats.codeforces_unsolved import CFUnsolvedProblems
from app.profile_stats.uva_unsolved import UvaUnsolvedProblems
from app.profile_stats.atcoder_unsolved import AtCoderUnsolvedProblems
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from builtins import str
from sqlalchemy import select

import requests
import json
import re
source = ''
cust_input = ''
language = ''
lang_version = ''
temp_source_code = ''
temp_source_code1 = ''
temp_language = ''
temp_code_name = ''
template_code_name = ''
temp_run_code = ''
temp_input = ''
handle_value = ''


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # permitted_languages = [("C", "C (gcc 4.8.1)"), ("CPP", "C++ (g++ 4.8.1)"), ("CSHARP", "C#"), \
    #             ("CLOJURE", "Clojure (clojure 1.1.0)"), ("CSS", "CSS"), ("HASKELL", "Haskell (ghc 7.4.1)"), \
    #             ("JAVA", "Java (openjdk 1.7.0_09)"), ("JAVASCRIPT", "JavaScript"), ("OBJECTIVEC", "Objective-C (clang 3.3)"), \
    #             ("PERL", "Perl (perl 5.14.2)"), ("PHP", "PHP (php 5.3.10)"), ("PYTHON", "Python (python 2.7.3)"), \
    #             ("R", "R (RScript 2.14.1)"), ("RUBY", "Ruby (ruby 2.1.1)"), ("RUST", "Rust (rustc 1.4.0)"), ("SCALA", "Scala (scalac 2.9.1)")
    # ]
    permitted_languages = [("c", "C (gcc 4.8.1)"), ("cpp17", "C++ (g++ 4.8.1)"), ("csharp", "C#"),
                           ("clojure", "Clojure (clojure 1.1.0)"), ("bash",
                                                                    "Bash Shell 5.0.11"), ("haskell", "Haskell (ghc 7.4.1)"),
                           ("java", "Java (openjdk 1.7.0_09)"), ("nodejs",
                                                                 "JavaScript"), ("objc", "Objective-C (clang 3.3)"),
                           ("perl", "Perl (perl 5.14.2)"), ("php",
                                                            "PHP (php 5.3.10)"), ("python3", "Python (python 2.7.3)"),
                           ("dart", "Dart (Dart 2.5.1)"), ("ruby", "Ruby (ruby 2.1.1)"), ("rust",
                                                                                          "Rust (rustc 1.4.0)"), ("scala", "Scala (scalac 2.9.1)"),
                           ("go", "Go 1.13.1"), ('brainfuck', 'Brainf**k (bfc-0.1)'), ('lua',
                                                                                       'Lua 5.3.5'), ('kotlin', 'Kotlin 1.3.50')
                           ]

    form = SubmissionForm()
    form.language.choices = permitted_languages

    if form.validate_on_submit():
        global source
        source = form.source_code.data
        # print(source)
        global cust_input
        cust_input = form.custom_input.data
        global temp_code_name
        temp_code_name = form.code_name.data
        global template_code_name
        template_code_name = form.code_name.data
        global language
        language = form.language.data
        if form.compile_code.data:
            return redirect(url_for('compile'))
        elif form.run_code.data:
            return redirect(url_for('run'))
        elif form.save_code.data:
            if not (current_user.is_authenticated):
                global temp_source_code
                temp_source_code = source
                flash('You need to login first')
                return redirect(url_for('login'))
            else:
                user = User.query.filter_by(username=current_user.username).first()
                code = SaveCode(code_name=temp_code_name, source_code=source, coder=user)
                # get_code_name = SaveCode(code_name=temp_code_name, coder=user)
                flash('Saved')
                db.session.add(code)
                # db.session.add(get_code_name)
                db.session.commit()

        elif form.save_template.data:
            if not (current_user.is_authenticated):
                global temp_source_code1
                temp_source_code1 = source
                flash('You need to login first')
                return redirect(url_for('login'))
            else:
                user = User.query.filter_by(username=current_user.username).first()
                temp_code = tempCode(code_name=template_code_name, temp_code=source, coder=user)
                flash('Template saved!')
                db.session.add(temp_code)
                db.session.commit()

    # for save codes
    if request.method == 'GET' and temp_source_code:
        form.source_code.data = temp_source_code
        if hasattr(current_user, 'username'):
            user = User.query.filter_by(username=current_user.username).first()
            code = SaveCode(code_name=temp_code_name, source_code=temp_source_code, coder=user)
            # get_code_name = SaveCode(code_name=temp_code_name, coder=user)
            db.session.add(code)
            # db.session.add(get_code_name)
            db.session.commit()
            flash("Saved!")
        temp_source_code = ''
        temp_code_name = ''

    return render_template('index.html', form=form)

    # for code_templates
    if request.method == 'GET' and temp_source_code1:
        form.source_code.data = temp_source_code1
        if hasattr(current_user, 'username'):
            user = User.query.filter_by(username=current_user.username).first()
            # temp_code = tempCode(temp_code=source, coder=user)
            temp_code = tempCode(code_name=template_code_name,
                                 source_code=temp_source_code1, coder=user)
            db.session.add(temp_code)
            db.session.commit()
            flash("Template saved!")
        temp_source_code1 = ''
        template_code_name = ''

    return render_template('index.html', form=form)


@app.route('/compile/')
def compile():
    # data = {
    #     'client_secret': Config.CLIENT_SECRET_KEY,
    #     'async': 0,
    #     'source': source,
    #     'lang': language,
    #     'time_limit': 5,
    #     'memory_limit': 262144,
    # }
    LANG_CODE = {
        'c': 4, 'java': 3, 'cpp17': 3, 'python3': 3, 'go': 3,
        'sql': 3, 'csharp': 3, 'dart': 3, 'nodejs': 3, 'kotlin': 2, 'brainfuck': 0, "clojure": 2, "haskell": 3, "objc": 3, "perl": 3, "php": 3,
        "ruby": 3, "rust": 3, "scala": 3, 'bash': 3, 'lua': 2
    }


    data = {
        'clientId': Config.CLIENT_ID,
        'clientSecret': Config.CLIENT_SECRET_KEY,
        'script': source,
        'stdin': '',
        'language': language,
        'versionIndex': LANG_CODE[language],
    }

    headers = {'Content-type': 'application/json'}
    global temp_run_code
    global temp_input
    temp_run_code = data['script']
    print(temp_run_code)

    if cust_input:
        data['stdin'] = cust_input
        temp_input = data['stdin']
    print(temp_run_code)

    # r = requests.post(Config.COMPILE_URL, data=data)
    r = requests.post(url=Config.COMPILE_URL, data=json.dumps(data), headers=headers)
    # x = json.loads(r.text)
    x = r.json()
    print(x['statusCode'])

    return render_template('compile.html', result=x, form=form, content=temp_run_code, temp_input=temp_input)


@app.route('/run')
def run():
    # data = {
    #     'client_secret': Config.CLIENT_SECRET_KEY,
    #     'async': 0,
    #     'source': source,
    #     'lang': language,
    #     'time_limit': 5,
    #     'memory_limit': 262144,
    # }

    LANG_CODE = {
        'c': 4, 'java': 3, 'cpp17': 0, 'python3': 3, 'go': 3,
        'sql': 3, 'csharp': 3, 'dart': 3, 'nodejs': 3, 'kotlin': 2, 'brainfuck': 0, "clojure": 2, "haskell": 3, "objc": 3, "perl": 3, "php": 3,
        "ruby": 3, "rust": 3, "scala": 3, 'bash': 3, 'lua': 2
    }

    data = {
        'clientId': Config.CLIENT_ID,
        'clientSecret': Config.CLIENT_SECRET_KEY,
        'script': source,
        'stdin': '',
        'language': language,
        'versionIndex': LANG_CODE[language],
    }
    #headers = {"content-type": "application/json", "client-secret": Config.CLIENT_SECRET_KEY}
    headers = {'Content-type': 'application/json'}

    form = SubmissionForm()

    global temp_run_code
    global temp_input
    temp_run_code = data['script']
    print(temp_run_code)

    if cust_input:
        data['input'] = cust_input
        temp_input = data['input']

    print(temp_input)

    #r = requests.post(Config.RUN_URL, data=data)
    print(Config.CLIENT_SECRET_KEY)
    #r = requests.post(Config.RUN_URL, json=data, headers=headers)
    r = requests.post(url = Config.RUN_URL, data = json.dumps(data), headers = headers)
    #print(r.text)
    #x = json.loads(r.text)
    x = r.json()
    # x = {
    #         "result": {
    #             "run_status": {
    #                 "memory_used": "3392",
    #                 "status": "AC",
    #                 "time_used": "0.033403",
    #                 "signal": "OTHER",
    #                 "exit_code": "0",
    #                 "status_detail": "NA",
    #                 "stderr": "",
    #                 "output": "Hello,World!\nasdasdasdasd",
    #                 "request_NOT_OK_reason": "",
    #                 "request_OK": "True"
    #             },
    #         "compile_status": "OK"
    #     }
    # }
    print(x)
    return render_template('run.html', result=x, content=temp_run_code, temp_input=temp_input)

    # r = requests.post(Config.RUN_URL, data=data)
    # x = json.loads(r.text)
    # return render_template('run.html', result=x, content=temp_run_code, temp_input=temp_input)


# @app.route('/run')
# def run():
#     data = {
#     'client_secret': Config.CLIENT_SECRET_KEY,
#     'async': 0,
#     'source': source,
#     'lang': language,
#     'time_limit': 5,
#     'memory_limit': 262144,
#     }
#     if cust_input:
#         data['input'] = cust_input

#     r = requests.post(Config.RUN_URL, data=data)
#     x = json.loads(r.text)
#     return render_template('run.html', result=x)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print("first one " + form.username.data + form.password.data)
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        print(form.password.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('logged out')
    global temp_source_code
    temp_source_code = ''
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you are now a register user')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/saved')
def saved():
    user = User.query.filter_by(username=current_user.username).first()
    codes = user.save_codes.all()
    print(codes)
    if len(codes) == 0:
        return render_template('previous_saved.html', content="")

    recent_saved = codes
    print(recent_saved)

    # for item in codes:
    #     separated = item.split('-----')
    #     print(separated)

    return render_template('previous_saved.html', content=recent_saved)

    # while (int i==1):
    #     recent_saved = codes[-i]
    #     return render_template('previous_saved.html', content=recent_saved.source_code)
    #     i+=1;
    #     if(codes[-i]=="") break

    # recent_saved = codes[-1]
    # return render_template('previous_saved.html', content=recent_saved.source_code)


@app.route('/template')
def template():
    user = User.query.filter_by(username=current_user.username).first()
    temp_codes = user.temp_codes.all()
    if len(temp_codes) == 0:
        return render_template('code_templates.html', content="")

    recent_temp = temp_codes

    print(recent_temp)
    return render_template('code_templates.html', content=recent_temp)


@app.route('/upcomingContests')
def upcomingContests():
    # return render_template('upcomingContests.html')
    ccContests = CodeChef().getFutureContests()
    #  cfContests = CodeForces().getFutureContests()
    cfContests = ccContests
    ccNoC = len(ccContests)
    #  cfNoC = len(cfContests["Name"])
    cfNoC = ccNoC
    # print(ccContests)
    # print(cfContests)
    #  return render_template('upcomingContests.html', username = current_user.username, ccNoC = ccNoC, ccContests = ccContests, cfNoC = cfNoC, cfContests = cfContests)
    if not (current_user.is_authenticated):
        return render_template('upcomingContests.html', username='Anonymous', ccNoC=ccNoC, ccContests=ccContests, cfNoC=cfNoC, cfContests=cfContests)
    else:
        return render_template('upcomingContests.html', username=current_user.username, ccNoC=ccNoC, ccContests=ccContests, cfNoC=cfNoC, cfContests=cfContests)


@app.route('/profileStatistics', methods=['GET', 'POST'])
def profileStatistics():

    form = ProfileForm()

    return render_template('profile_statistics.html', form=form)


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    form = ProfileForm()
    global handle_value

    if form.validate_on_submit():

        print("hello")
        if form.codeforces.data:
            codeforces_scrapper = CodeforcesScrapper()
            handle_value = form.handle_name.data

            resp = codeforces_scrapper.get_user_rating_history(handle_value)
            resp3 = codeforces_scrapper.get_submission_stat_count(handle_value)
            userratings = []

            for item in resp:
                userratings.append(item['newRating'])

            print(userratings)
            data = userratings

            solved_count = resp3['solved_count']
            wrong_answer_count = resp3['wrong_answer_count']
            time_limit_exceeded_count = resp3['time_limit_exceeded_count']
            memory_limit_exceeded_count = resp3['memory_limit_exceeded_count']
            runtime_error_count = resp3['runtime_error_count']
            compilation_error_count = resp3['compilation_error_count']
            other_verdict_count = resp3['other_verdict_count']

            verdict_list = []
            verdict_list.append(solved_count)
            verdict_list.append(wrong_answer_count)
            verdict_list.append(time_limit_exceeded_count)
            verdict_list.append(memory_limit_exceeded_count)
            verdict_list.append(runtime_error_count)
            verdict_list.append(compilation_error_count)
            verdict_list.append(other_verdict_count)
            verdict_list.append(0)

            print(verdict_list)
            print(form.codeforces.data)
            print(handle_value)
            print("hello123")

            # fetching codeforces unsolved
            codeforces_unsolved = CFUnsolvedProblems()
            resp_unsolved_cf = codeforces_unsolved.get_codeforces_unsolved(handle_value)
            resp_get_submission_count_per_day = codeforces_unsolved.get_submission_count_per_day(handle_value)

            unsolved_problems = []
            submission_count = []
            unsolved_problems = resp_unsolved_cf['unsolved_problems']
            submission_count = resp_get_submission_count_per_day['subcountmap']
            print(unsolved_problems)
            print(submission_count)
            # print(unsolved_problems)
            # unsolved_problems_id = []
            # for item in resp_unsolved_cf['unsolved_problems']:
            #     unsolved_problems_id.append(item[0])

            # print(unsolved_problems_id)

            # unsolved_problems_name =[]
            # for item in resp['unsolved_problems']:
            #     unsolved_problems_name.append(item[1])

            # print(unsolved_problems_name)

            # unsolved_problems_links = []
            # for item in resp['unsolved_problems']:
            #     unsolved_problems_links.append(item[2])

            # print(unsolved_problems_links)

            # unsolved_problems_tags = []
            # for item in resp['unsolved_problems']:
            #     unsolved_problems_tags.append(item[3])

            # print(unsolved_problems_tags)

            return render_template('graph.html', rating_list=data, verdict_list=verdict_list, judge_name='CodeForces', handle_value=handle_value, unsolved_problems=unsolved_problems, submission_count=submission_count)

        if form.uva.data:
            uva_scrapper = UvaScrapper()
            handle_value = form.handle_name.data

            resp4 = uva_scrapper.get_user_submission_stat_count(handle_value)

            solved_count = resp4['solved_count']
            wrong_answer_count = resp4['wrong_answer_count']
            time_limit_exceeded_count = resp4['time_limit_exceeded_count']
            memory_limit_exceeded_count = resp4['memory_limit_exceeded_count']
            runtime_error_count = resp4['runtime_error_count']
            compilation_error_count = resp4['compilation_error_count']
            other_verdict_count = resp4['other_verdict_count']
            presentation_error_count = resp4['presentation_error_count']

            verdict_list = []
            verdict_list.append(solved_count)
            verdict_list.append(wrong_answer_count)
            verdict_list.append(time_limit_exceeded_count)
            verdict_list.append(memory_limit_exceeded_count)
            verdict_list.append(runtime_error_count)
            verdict_list.append(compilation_error_count)
            verdict_list.append(other_verdict_count)
            verdict_list.append(presentation_error_count)

            # uva unsolved problems
            uva_unsolved = UvaUnsolvedProblems()
            resp_unsolved_uva = uva_unsolved.get_unsolved_problems(handle_value)
            resp_get_submission_count_per_day = uva_unsolved.get_submission_count_per_day(handle_value)

            unsolved_problems = []
            submission_count = []
            unsolved_problems = resp_unsolved_uva['unsolved_problems']
            submission_count = resp_get_submission_count_per_day['subcountmap']
            print(unsolved_problems)
            print(submission_count)
            print(verdict_list)

            return render_template('graph.html', verdict_list=verdict_list, judge_name='UVa', handle_value=handle_value, unsolved_problems=unsolved_problems, submission_count=submission_count)

        if form.codechef.data:
            codechef_scrapper = CodeChefScrapper()
            handle_value = form.handle_name.data

            resp5 = codechef_scrapper.getRatingHistory(handle_value)

            userratings = []

            for item in resp5['date_versus_rating']['all']:
                userratings.append(int(item['rating']))

            print(userratings)

            return render_template('graph.html', rating_list=userratings, judge_name='CodeChef', handle_value=handle_value)

        if form.spoj.data:
            spoj_scrapper = SpojScrapper()
            handle_value = form.handle_name.data

            resp6 = spoj_scrapper.get_submission_stat_count(handle_value)

            solved_count = resp6['solved_count']
            wrong_answer_count = resp6['wrong_answer_count']
            time_limit_exceeded_count = resp6['time_limit_exceeded_count']
            memory_limit_exceeded_count = resp6['memory_limit_exceeded_count']
            runtime_error_count = resp6['runtime_error1_count'] + \
                resp6['runtime_error2_count']
            compilation_error_count = resp6['compilation_error_count']
            other_verdict_count = resp6['other_verdict_count']

            verdict_list = []
            verdict_list.append(solved_count)
            verdict_list.append(wrong_answer_count)
            verdict_list.append(time_limit_exceeded_count)
            verdict_list.append(memory_limit_exceeded_count)
            verdict_list.append(runtime_error_count)
            verdict_list.append(compilation_error_count)
            verdict_list.append(other_verdict_count)
            verdict_list.append(0)

            # spoj unsolved problems
            spoj_unsolved = SPOJUnsolvedProblems()
            resp_unsolved_spoj = spoj_unsolved.get_unsolved_problems(handle_value)
            resp_get_submission_count_per_day = spoj_unsolved.get_submission_count_per_day(handle_value)

            unsolved_problems = []
            submission_count = []
            unsolved_problems = resp_unsolved_spoj['unsolved_problems']
            submission_count = resp_get_submission_count_per_day['subcountmap']

            return render_template('graph.html', verdict_list=verdict_list, judge_name='SPOJ', handle_value=handle_value, unsolved_problems=unsolved_problems, submission_count=submission_count)

        if form.atcoder.data:
            atcoder_scrapper = AtCoderScrapper()
            handle_value = form.handle_name.data

            resp7, resp8 = atcoder_scrapper.get_user_ratings(handle_value)
            userratings = []
            for item in resp8:
                userratings.append(item['NewRating'])

            print(userratings)

            resp9 = atcoder_scrapper.get_user_submission_count(handle_value)

            solved_count = resp9['solved_count']
            wrong_answer_count = resp9['wrong_answer_count']
            time_limit_exceeded_count = resp9['time_limit_exceeded_count']
            memory_limit_exceeded_count = resp9['memory_limit_exceeded_count']
            runtime_error_count = resp9['runtime_error_count']
            compilation_error_count = resp9['compilation_error_count']
            other_verdict_count = resp9['other_verdict_count']

            verdict_list = []
            verdict_list.append(solved_count)
            verdict_list.append(wrong_answer_count)
            verdict_list.append(time_limit_exceeded_count)
            verdict_list.append(memory_limit_exceeded_count)
            verdict_list.append(runtime_error_count)
            verdict_list.append(compilation_error_count)
            verdict_list.append(other_verdict_count)
            verdict_list.append(0)

            # atcoder unsolved problems
            atcoder_unsolved = AtCoderUnsolvedProblems()
            resp_unsolved_atcoder = atcoder_unsolved.get_unsolved_problems(handle_value)
            resp_get_submission_count_per_day = atcoder_unsolved.get_submission_count_per_day(handle_value)

            unsolved_problems = []
            submission_count = []
            unsolved_problems = resp_unsolved_atcoder['unsolved_problems']
            submission_count = resp_get_submission_count_per_day['subcountmap']

            return render_template('graph.html', rating_list=userratings, verdict_list=verdict_list, judge_name='AtCoder', handle_value=handle_value, unsolved_problems=unsolved_problems, submission_count=submission_count)

    return render_template('graph.html', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: {url_for('reset_token', token=token, _external=True)}
                    If you did not make this request then simply ignore this email and no changes will be made.
                '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

# @app.route('/reset_request', methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))

#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email = form.email.data).first()
#         user.set_password(form.password.data)
#         db.session.commit()
#         print(user)
#         # user = User.query.filter_by(email = form.email.data).first()
#         flash('Your password has been updated! You are now able to log in')
#         return redirect(url_for('login'))

#     return render_template('reset_request.html', form=form)

# @app.route('/reset_password/<user>', methods=['GET', 'POST'])
# def reset_password(user):
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))

#     print(user)
#     if user is None:
#         flash('That is an invalid email', 'warning')
#         return redirect(url_for('reset_request'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         password = form.password.data
#         User.set_password(user, password)
#         db.session.commit()
#         flash('Your password has been updated! You are now able to log in')
#         return redirect(url_for('login'))
#     return render_template('reset_token.html', form=form)


@app.route('/algorithm', methods=['GET', 'POST'])
def algorithm():
    permitted_type = [
        (1, "String"), (2, "Graph"), (3, "Number Theory"), (4, "Data Structure"), (5, "Greedy"),
        (6, "Geometry"), (7, "Game Theory"), (8, "Dynamic Programming"), (9, "Linear Algebra"),
        (10, "Combinatorics"), (11, "Miscellaneous")
    ]

    permitted_proficiency = [
        (1, "Novice"), (2, "Somewhat Good"), (3, "Good"), (4, "Expert")
    ]

    # if not current_user.is_authenticated:
    #     return redirect(url_for('index'))

    # if current_user.is_authenticated:
    #     return redirect(url_for('algorithm'))

    form = AlgorithmForm()
    form.algo_proficiency.choices = permitted_proficiency
    form.algo_type.choices = permitted_type

    if form.validate_on_submit():
        algorithm = Algorithm(algo_name=form.algo_name.data, algo_resources=form.algo_resources.data, algo_problems=form.algo_problems.data, algo_proficiency=form.algo_proficiency.data, algo_type=form.algo_type.data, user_id=current_user.id)
        db.session.add(algorithm)
        db.session.commit()
        print("here inside!")
        flash('Algorithm added succesfully!')
        return redirect(url_for('algorithm_list'))

    return render_template('algorithm.html', form=form)


@app.route('/algorithm_list', methods=['GET', 'POST'])
def algorithm_list():

    permitted_type = [
        (1, "String"), (2, "Graph"), (3, "Number Theory"), (4, "Data Structure"), (5, "Greedy"),
        (6, "Geometry"), (7, "Game Theory"), (8, "Dynamic Programming"), (9, "Linear Algebra"),
        (10, "Combinatorics"), (11, "Miscellaneous")
    ]

    permitted_proficiency = [
        (1, "Novice"), (2, "Somewhat Good"), (3, "Good"), (4, "Expert")
    ]

    form = AlgorithmForm()
    form.algo_proficiency.choices = permitted_proficiency
    form.algo_type.choices = permitted_type

    if form.validate_on_submit():
        algorithm = Algorithm(algo_name=form.algo_name.data, algo_resources=form.algo_resources.data, algo_problems=form.algo_problems.data, algo_proficiency=form.algo_proficiency.data, algo_type=form.algo_type.data, user_id=current_user.id)
        db.session.add(algorithm)
        db.session.commit()
        print("here inside!")
        flash('Algorithm added succesfully!')
        return redirect(url_for('algorithm_list'))

    user = User.query.filter_by(username=current_user.username).first()
    algorithm_table = user.algorithm_table.all()

    print(algorithm_table)
    if len(algorithm_table) == 0:
        flash("Add an algorithm to the table first")
    return render_template('algorithm_table.html', algorithms=algorithm_table, form = form)


@app.route('/edit_algo/<got_id>', methods=['GET', 'POST'])
def edit_algo(got_id):

    stmnt = Algorithm.query.filter_by(algorithm_id=got_id).first()
    print("The id is: " + got_id)

    if request.method == 'POST':

        get = Algorithm.query.get(request.form.get('id'))

        print(get)
        get.algo_name = request.form['algo_name']
        get.algo_resources = request.form['algo_resources']
        get.algo_problems = request.form['algo_problems']
        db.session.commit()

        user = User.query.filter_by(username=current_user.username).first()
        algorithm_table = user.algorithm_table.all()

        return render_template('algorithm_table.html', algorithms=algorithm_table)


@app.route('/delete_algo/<got_id>', methods=['GET', 'POST'])
def delete_algo(got_id):

    # stmnt = Algorithm.query.filter_by(algorithm_id = got_id).first()
    print("The id is: " + got_id)

    get = Algorithm.query.get(got_id)
    print(get)
    db.session.delete(get)
    db.session.commit()
    flash('Algorithm Deleted successfully!')
    user = User.query.filter_by(username=current_user.username).first()
    algorithm_table = user.algorithm_table.all()

    return render_template('algorithm_table.html', algorithms=algorithm_table)


@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(message)

    return dict(mdebug=print_in_console)
