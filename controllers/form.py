from flask.ext.wtf import Form

from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import StringField

from wtforms.validators import DataRequired

class SimForm(Form):

  replications = IntegerField('replications', validators=[DataRequired()])
  simulation_horizon = IntegerField('simulation_horizon', validators=[DataRequired()])
  trucks_amount = IntegerField('trucks_amount', validators=[DataRequired()])
  trucks_use = IntegerField('trucks_use', validators=[DataRequired()])
  workshop_capacity = IntegerField('workshop_capacity', validators=[DataRequired()])
  components = IntegerField('components', validators=[DataRequired()])

  component_name = StringField('component_name', validators=[DataRequired()])

  distributions = SelectField(u'Distribución', choices=[('1', 'Poisson'), 
    ('2', 'Exponencial'), ('3', 'Weibull')], validators=[DataRequired()])

  failure_distr = distributions
  failure_param = IntegerField('failure_param', validators=[DataRequired()])  

  initial_stock = IntegerField('initial_stock', validators=[DataRequired()])

  work_distr = distributions
  work_param = IntegerField('failure_param', validators=[DataRequired()])

  repl_distr = distributions
  repl_param = IntegerField('repl_param', validators=[DataRequired()])



  def form1():
    pass

  def form2():
    pass
