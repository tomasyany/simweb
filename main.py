import os.path
import json

from time import sleep

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash

from controllers.form import SimForm

from big_app import Simulation

app = Flask (__name__)

@app.route ('/')
def home():
  return render_template('welcome.html')

@app.route ('/form', methods=['GET', 'POST'])
def form(): 
  form = SimForm(request.form)
  if request.method == 'POST' and form.validate():
      data = request.form

      replications = int(data['replications'])
      total_trucks = int(data['trucks_amount'])
      design_number = int(data['trucks_use'])
      workshop_capacity = int(data['workshop_capacity'])
      simulation_horizon = int(data['simulation_horizon'])
      n_components = int(data['components'])

      comp_names = []
      life_dist_parameters = []
      repair_dist_parameters = []
      replacement_dist_parameters = []
      start_inventory = []
      for i in range(0, n_components):
        if i == 0:
          aux_comp_name = data['component_name']
          comp_names.append(aux_comp_name)

          aux = [data['failure_distr'], [int(data['failure_param'])]]
          life_dist_parameters.append(aux)

          aux = [data['work_distr'], [int(data['work_param'])]]
          repair_dist_parameters.append(aux)

          aux = [data['repl_distr'], [int(data['repl_param'])]]
          replacement_dist_parameters.append(aux)

          aux = int(data['initial_stock'])
          start_inventory.append(aux)

        if i > 0:
          aux_comp_name = data['component_name_'+str(i)]
          comp_names.append(aux_comp_name)

          aux = [data['failure_distr_'+str(i)], [int(data['failure_param_'+str(i)])]]
          life_dist_parameters.append(aux)

          aux = [data['work_distr_'+str(i)], [int(data['work_param_'+str(i)])]]
          repair_dist_parameters.append(aux)

          aux = [data['repl_distr_'+str(i)], [int(data['repl_param_'+str(i)])]]
          replacement_dist_parameters.append(aux)

          aux = int(data['initial_stock_'+str(i)])
          start_inventory.append(aux)

      my_sim = Simulation(replications, total_trucks, design_number,
                 workshop_capacity, n_components, comp_names,
                 life_dist_parameters, repair_dist_parameters,
                 replacement_dist_parameters, start_inventory,
                 simulation_horizon)
      my_sim.run_simulation()
      
      return redirect('/results1')
  return render_template('form.html', title='Setup', form=form)

@app.route ('/results1')
def results1():
  filename = "outputs/pie.csv"
  if os.path.isfile(filename):
    data_file = open(filename, 'r')
    pies = []
    titles = []
    headers = []
    for line_number, line in enumerate(data_file):
      line = line.split(',')

      if line_number == 0:
        titles.append('Distribución tiempos 1')
        headers.append([['string', 'Tiempo'], ['number', 'Utilización']])
        t = ["Tiempo Activo", 
             "Tiempo en Reparación", 
             "Tiempo en Stand-by"]

      elif line_number == 1:
        titles.append('Distribución tiempo cola y taller')
        headers.append([['string', 'Tiempo'], ['number', 'Utilización']])
        t = ["Tiempo en Espera Respuestos",
             "Tiempo en Espera Entrada Taller",
             "Tiempo en Taller"]

      elif line_number == 2: 
        titles.append('Distribución tiempos 2')
        headers.append([['string', 'Tiempo'], ['number', 'Utilización']])
        t = ["Tiempo Activo",
             "Tiempo en Cola",
             "Tiempo en Taller",
             "Tiempo en Stand-by"]

      elif line_number == 3: 
        titles.append('Proporción vehículos')
        headers.append([['string', 'Tiempo'], ['number', 'Utilización']])
        t = ["Vehículos activos",
             "Vehículos en Reparación",
             "Vehículos en Stand-by"]

      elif line_number == 4: 
        titles.append('Proporción vehículos cola y taller')
        headers.append([['string', 'Tiempo'], ['number', 'Utilización']])
        t = ["Vehículos en Espera Respuestos",
             "Vehículos en Espera Entrada Taller",
             "Vehículos en Taller"]

      pies.append([[name,float(value)] for name, value in zip(t, line)])
    return render_template('results1.html', title='Resultados 1',
                           pies=json.dumps(pies),
                           titles=json.dumps(titles),
                           headers=json.dumps(headers))
  else:
    return render_template('no_results.html', title='No hay resultados')

@app.route ('/results2')
def results2():
  filename = "outputs/bars.csv"
  if os.path.isfile(filename):
    data_file = open(filename, 'r')
    pies = []
    titles = []
    headers = []
    for line_number, line in enumerate(data_file):
      line = line.split(',')

      if line_number == 0:
        titles.append('Distribución tiempos 1')
        headers.append([['string', 'Tiempo'], ['number', 'Utilización']])
        t = ["Tiempo Activo", 
             "Tiempo en Reparación", 
             "Tiempo en Stand-by"]

      elif line_number == 1:
        titles.append('Distribución tiempo cola y taller')
        headers.append([['string', 'Tiempo'], ['number', 'Utilización']])
        t = ["Tiempo en Espera Respuestos",
             "Tiempo en Espera Entrada Taller",
             "Tiempo en Taller"]

      elif line_number == 2: 
        titles.append('Distribución tiempos 2')
        headers.append([['string', 'Tiempo'], ['number', 'Utilización']])
        t = ["Tiempo Activo",
             "Tiempo en Cola",
             "Tiempo en Taller",
             "Tiempo en Stand-by"]

      elif line_number == 3: 
        titles.append('Proporción vehículos')
        headers.append([['string', 'Tiempo'], ['number', 'Utilización']])
        t = ["Vehículos activos",
             "Vehículos en Reparación",
             "Vehículos en Stand-by"]

      elif line_number == 4: 
        titles.append('Proporción vehículos cola y taller')
        headers.append([['string', 'Tiempo'], ['number', 'Utilización']])
        t = ["Vehículos en Espera Respuestos",
             "Vehículos en Espera Entrada Taller",
             "Vehículos en Taller"]

      pies.append([[name,float(value)] for name, value in zip(t, line)])
    return render_template('results2.html', title='Resultados 2',
                           pies=json.dumps(pies),
                           titles=json.dumps(titles),
                           headers=json.dumps(headers))
  else:
    return render_template('no_results.html', title='No hay resultados')


if __name__ == "__main__":
  app.debug = True # NOT IN PRODUCTION
  app.config.from_object('config')

  app.run()
