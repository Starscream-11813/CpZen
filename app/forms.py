from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField, BooleanField, \
	StringField, PasswordField, SubmitField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.widgets.core import TextArea
from app.models import User
from flask_codemirror.fields import CodeMirrorField


class SubmissionForm(FlaskForm):
	language = SelectField('Language', validators=[DataRequired()])
	source_code = CodeMirrorField(language='clike', config={'lineNumbers' : 'true', 'tabSize': 4, 'indentUnit': 4, 'indentWithTabs': 'true', 'scrollbarStyle': 'simple', 'styleActiveLine': 'true', 'mode':'eclipse', 'matchBrackets': 'true', 'autoCloseTags': 'true', 'autoCloseBrackets': '(){}[]""', 'matchTags': 'true', 'lineWrapping': 'true', 'foldGutter':'true', 'autoMatchBrackets': 'true', 'showCursorWhenSelecting': 'true',  'gutters': ["CodeMirror-linenumbers", "CodeMirror-foldgutter"]})
	custom_input_check = BooleanField('Custom Input')
	compile_code = SubmitField('Compile (Alt+C)')
	run_code = SubmitField('Run (Alt+R)')
	#custom_input = TextAreaField()
	custom_input = CodeMirrorField(language='clike', config={'smartIndent': 'false', 'scrollbarStyle': 'simple', 'styleActiveLine': 'true'})
	save_code = SubmitField('Save (Alt+S)')
	save_template = SubmitField('Save as template (Alt+T)')
	code_name=TextField()
	



class ProfileForm(FlaskForm):
	#for profile stats
	codeforces = BooleanField("CodeForces")
	codechef = BooleanField("CodeChef")
	uva = BooleanField("UVa")
	atcoder = BooleanField("AtCoder")
	spoj = BooleanField("SPOJ")
	handle_name = StringField('Judge Handle', validators=[DataRequired()])
	get_stat = SubmitField("Let's Go!")



class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

# forgot pass forms
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')



# class RequestResetForm(FlaskForm):
# 	email = StringField('Email', validators=[DataRequired(), Email()])
# 	password = PasswordField('Password', validators=[DataRequired()])
# 	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
# 	submit = SubmitField('Reset Password')

# 	def validate_email(self, email):
# 		user = User.query.filter_by(email=email.data).first()
# 		if user is None:
# 			raise ValidationError('There is no account with that email. You must register first.')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Password2', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

# form for iputting algorithm
class AlgorithmForm(FlaskForm):
	algo_name = StringField('algo_name', validators=[DataRequired()])
	algo_resources = TextAreaField('algo_resources', validators=[DataRequired()])
	algo_problems = TextAreaField('algo_problems', validators=[DataRequired()])
	algo_proficiency = SelectField('algo_proficiency', validators=[DataRequired()])
	algo_type = SelectField('algo_type', validators=[DataRequired()])
	submit = SubmitField('Add the algorithm')

	