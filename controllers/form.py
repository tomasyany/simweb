from flask.ext.wtf import Form

from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import StringField

from wtforms.validators import DataRequired

class SimForm(Form):

  replications = IntegerField('replications', validators=[DataRequired()])
  simulation_horizon = IntegerField('simulation_horizon', validators=[DataRequired()])
  trucks_amount = IntegerField('trucks_amount', validators=[DataRequired()])
  # trucks_use = IntegerField('trucks_use', validators=[DataRequired])
  # workshop_capacity = IntegerField('workshop_capacity', validators=[DataRequired])
  # components = IntegerField('components', validators=[DataRequired])

  # lifetime_mean # tiempo de vida medio de una componente
  # repairtime_mean
  # replacementetime_mean # tiempo de reposición
  # start_inventory # inventario inicial por componente

  # componentes_id # nombre de componente

  # distribucion_componente
  # distribucion_componente
  # distribucion_componente


  def form1():
    pass

  def form2():
    pass
