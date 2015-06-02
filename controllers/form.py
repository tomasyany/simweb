from wtforms import Form

from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import TextField

from wtforms import validators

class SimForm(Form):

  sim_name = TextField('simulation_name', [validators.InputRequired()])
  replications = IntegerField('replications', [validators.InputRequired()])
  simulation_horizon = IntegerField('simulation_horizon', [validators.InputRequired()])
  trucks_amount = IntegerField('trucks_amount', [validators.InputRequired()])
  trucks_use = IntegerField('trucks_use', [validators.InputRequired()])
  workshop_capacity = IntegerField('workshop_capacity', [validators.InputRequired()])
  components = IntegerField('components', [validators.InputRequired()])

  component_name = TextField('component_name', [validators.InputRequired()])


  distributions = [('poisson', 'Poisson'), 
    ('exponential', 'Exponencial'), ('weibull', 'Weibull')]

  failure_distr =  SelectField(u'Distribución',[validators.InputRequired()], choices=distributions)
  failure_param = IntegerField('failure_param', [validators.InputRequired()])

  initial_stock = IntegerField('initial_stock', [validators.InputRequired()])

  work_distr = SelectField(u'Distribución',[validators.InputRequired()], choices=distributions)
  work_param = IntegerField('failure_param', [validators.InputRequired()])

  repl_distr = SelectField(u'Distribución',[validators.InputRequired()], choices=distributions)
  repl_param = IntegerField('repl_param', [validators.InputRequired()])
