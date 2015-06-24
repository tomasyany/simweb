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
      my_sim.print_pie_file()
      my_sim.print_time_evolution_files()
      my_sim.print_bars_file()
      
      return redirect('/results1')
  return render_template('form.html', title='Setup', form=form)

@app.route ('/results1')
def results1():
  filename = "outputs/pie.csv"
  if os.path.isfile(filename):
    data_file = open(filename, 'r')
    values = []
    titles = []
    headers = []
    for line_number, line in enumerate(data_file):
      line = line.strip().split(',')

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

      values.append([[name,float(value)] for name, value in zip(t, line)])
    return render_template('results1.html', title='Resultados 1',
                           values=json.dumps(values),
                           titles=json.dumps(titles),
                           headers=json.dumps(headers))
  else:
    return render_template('no_results.html', title='No hay resultados')

@app.route ('/results2')
def results2():
  filename = "outputs/bars.csv"
  if os.path.isfile(filename):
    data_file = open(filename, 'r')
    values = []
    titles = []
    headers = []
    
    for line_number, line in enumerate(data_file):
      line = line.strip().split(',')

      if line_number == 0:
        titles.append('Porcentaje Ocupación Plazas Taller')
        headers.append([['string', 'Plaza'], ['number', 'Ocupación']])
        t = []
        for i in line:
          t.append("Plaza "+str(i))

      elif line_number == 1:
        values.append([[name,float(value)] for name, value in zip(t, line)])

      elif line_number == 2:
        titles.append('Fallas promedio por componente')
        headers.append([['string', 'Componente'], ['number', 'Fallas']])
        t = [] 
        for i in line:
          t.append(i)

      elif line_number == 3: 
        values.append([[name,float(value)] for name, value in zip(t, line)])

      elif line_number == 4: 
        titles.append('Inventario promedio por componente')
        headers.append([['string', 'Componente'], ['number', 'Inventario']])
        values.append([[name,float(value)] for name, value in zip(t, line)])

      elif line_number == 5: 
        titles.append('No respuesta de inventario por componente')
        headers.append([['string', 'Componente'], ['number', 'Proporción de veces']])
        values.append([[name,float(value)] for name, value in zip(t, line)])      
      
    return render_template('results2.html', title='Resultados 2',
                           values=json.dumps(values),
                           titles=json.dumps(titles),
                           headers=json.dumps(headers))
  else:
    return render_template('no_results.html', title='No hay resultados')

@app.route ('/results3')
def results3():
  filenames = []

  filenames.append("outputs/time_evolution_1.csv")
  filenames.append("outputs/time_evolution_2.csv")
  filenames.append("outputs/time_evolution_3.csv")
  filenames.append("outputs/time_evolution_4.csv")
  filenames.append("outputs/time_evolution_5.csv")

  if False not in [os.path.isfile(f) for f in filenames]:
    data_files = [open(f, 'r') for f in filenames]
    values = []
    titles = []
    for i, current_file in enumerate(data_files):
      current_value = []
      if i == 0:
        titles.append('Evolución del estado de los vehículos')
        current_value.append(['Tiempo', 
                       'Vehículos activos',
                       'Vehículos en reparación',
                       'Vehículos en stand-by'])

      elif i == 1:
        titles.append('Evolución de la cola por espera de respuestos')
        current_value.append(['Tiempo', 
                       'Vehículos en cola'])
      elif i == 2:
        titles.append('Evolución de la cola de entrada al taller')
        current_value.append(['Tiempo', 
                       'Vehículos en cola'])
      elif i == 3:
        titles.append('Evolución de vehículos dentro del taller')
        current_value.append(['Tiempo', 
                       'Vehículos en taller'])
      elif i == 4:
        titles.append('Evolución del inventario por componente')
        line = current_file.readline()
        line = line.strip().split(',')
        current_value.append(line)

      for line in current_file.readlines():
        line = line.strip().split(',')
        line = [float(i) for i in line]
        current_value.append(line)

      values.append(current_value)
    return render_template('results3.html', title='Resultados 3',
                        values=json.dumps(values),
                        titles=json.dumps(titles))

  else:
    return render_template('no_results.html', title='No hay resultados')

@app.route ('/results4')
def results4():
  filename = "outputs/summary.csv"
  if os.path.isfile(filename):
    data_file = open(filename, 'r')
    values = []
    headers = []
    titles = []
    
    for line_number, line in enumerate(data_file):
      line = line.strip().split(',')

      if line_number == 0:
        headers = line 

      else:
        line = [float(k) if i>0 else k for i,k in enumerate(line)]
        values.append(line)  
    
    titles.append("Proporciones de tiempos e intervalos de confianza (95%)")
    titles.append("Número promedio de vehículos e intervalos de confianza(95%)")
    titles.append("Número promedio de fallas por componente e intervalos de confianza(95%)")

    return render_template('results4.html', title='Resultados 4',
                           values=json.dumps(values),
                           titles=json.dumps(titles),
                           headers=json.dumps(headers))
  else:
    return render_template('no_results.html', title='No hay resultados')

if __name__ == "__main__":
  app.debug = True # NOT IN PRODUCTION
  app.config.from_object('config')

  app.run()
