from wtforms import Form

from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import StringField
from wtforms import DecimalField

from wtforms import validators

class SimForm(Form):

  sim_name = StringField('simulation_name', [validators.InputRequired()])
  replications = IntegerField('replications', [validators.InputRequired()])
  simulation_horizon = IntegerField('simulation_horizon', [validators.InputRequired()])
  trucks_amount = IntegerField('trucks_amount', [validators.InputRequired()])
  trucks_use = IntegerField('trucks_use', [validators.InputRequired()])
  workshop_capacity = IntegerField('workshop_capacity', [validators.InputRequired()])
  components = IntegerField('components', [validators.InputRequired()])

  component_name = StringField('component_name', [validators.InputRequired()])


  distributions = [('poisson', 'Poisson'), 
    ('exponential', 'Exponencial'), ('normal', 'Normal'), ('uniform', 'Uniforme'), 
    ('binomial', 'Binomial'), ('geometric', 'Geométrica'), ('gamma', 'Gamma'), 
    ('beta', 'Beta'), ('lognormal', 'Log Normal'), ('weibull', 'Weibull')]

  failure_distr =  SelectField(u'Distribución',[validators.InputRequired()], choices=distributions)
  failure_param_1 = DecimalField('failure_param', [validators.Optional()])
  failure_param_2 = DecimalField('failure_param', [validators.Optional()])

  initial_stock = DecimalField('initial_stock', [validators.InputRequired()])

  work_distr = SelectField(u'Distribución',[validators.InputRequired()], choices=distributions)
  work_param_1 = DecimalField('work_param', [validators.Optional()])
  work_param_2 = DecimalField('work_param', [validators.Optional()])

  repl_distr = SelectField(u'Distribución',[validators.InputRequired()], choices=distributions)
  repl_param_1 = DecimalField('repl_param', [validators.Optional()])
  repl_param_2 = DecimalField('repl_param', [validators.Optional()])
