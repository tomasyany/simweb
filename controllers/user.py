from wtforms import Form

from wtforms import TextField

from wtforms import validators

class LoginForm(Form):
  username = TextField('username', [validators.InputRequired()])
  
