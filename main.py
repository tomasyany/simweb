import os.path
import json
import sys
sys.stdout = open(os.devnull, "w") # Stops Python from printing stuff on console
import unicodedata
from string import ascii_letters

from time import sleep
import datetime
import shutil

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import session
from flask import url_for

from controllers.form import SimForm
from controllers.user import LoginForm

from big_app import Simulation

app = Flask (__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KTasd'

def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) 
                   if x in ascii_letters).lower()

@app.route ('/')
def home():
  return render_template('welcome.html', title="Welcome")

@app.route ('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm(request.form)
  if session.get('logged_in'):
    return redirect('/form')

  if request.method == 'POST' and form.validate():

    time = datetime.datetime.now().strftime('_%Y_%m_%d-%H_%M_%S')
    username = remove_accents(request.form['username']) + time
    directory = 'outputs/' + username
    session['username']  = username
    session['logged_in'] = True
    if not os.path.exists(directory):
        os.makedirs(directory)

    return redirect('/form')
  return render_template('login.html', title='Login', form=form)

@app.route('/clear')
def clearsession():
    username = session['username']
    directory = 'outputs/' + username
    if os.path.exists(directory):
      shutil.rmtree(directory)
    session.pop('logged_in', None)

    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('home'))

@app.route ('/form', methods=['GET', 'POST'])
def form(): 
  if not session.get('logged_in'):
    return render_template('no_results.html', title='No hay resultados')
  form = SimForm(request.form)
  username = session['username']
  if request.method == 'POST' and form.validate():
      data = request.form
      print (data)

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

          p1 = int(data['failure_param_1'])
          p2 = 0
          if 'failure_param_2' in data:
            p2 = int(data['failure_param_2'])
          aux = [data['failure_distr'], [p1,p2]]
          life_dist_parameters.append(aux)

          p1 = int(data['work_param_1'])
          p2 = 0
          if 'work_param_2' in data:
            p2 = int(data['work_param_2'])
          aux = [data['work_distr'], [p1,p2]]
          repair_dist_parameters.append(aux)

          p1 = int(data['repl_param_1'])
          p2 = 0
          if 'repl_param_2' in data:
            p2 = int(data['repl_param_2'])
          aux = [data['repl_distr'], [p1,p2]]
          replacement_dist_parameters.append(aux)

          aux = int(data['initial_stock'])
          start_inventory.append(aux)
        if i > 0:
          aux_comp_name = data['component_name_'+str(i)]
          comp_names.append(aux_comp_name)

          p1 = int(data['failure_param_1_'+str(i)])
          p2 = 0
          if 'failure_param_2_'+str(i) in data:
            p2 = int(data['failure_param_2_'+str(i)])
          aux = [data['failure_distr_'+str(i)], [p1,p2]]
          life_dist_parameters.append(aux)

          p1 = int(data['work_param_1_'+str(i)])
          p2 = 0
          if 'work_param_2_'+str(i) in data:
            p2 = int(data['work_param_2_'+str(i)])
          aux = [data['work_distr_'+str(i)], [p1,p2]]
          repair_dist_parameters.append(aux)

          p1 = int(data['repl_param_1_'+str(i)])
          p2 = 0
          if 'repl_param_2_'+str(i) in data:
            p2 = int(data['repl_param_2_'+str(i)])
          aux = [data['repl_distr_'+str(i)], [p1,p2]]
          replacement_dist_parameters.append(aux)

          aux = int(data['initial_stock_'+str(i)])
          start_inventory.append(aux)

      my_sim = Simulation(replications, total_trucks, design_number,
                 workshop_capacity, n_components, comp_names,
                 life_dist_parameters, repair_dist_parameters,
                 replacement_dist_parameters, start_inventory,
                 simulation_horizon, username)
      my_sim.run_simulation()
      my_sim.print_pie_file()
      my_sim.print_time_evolution_files()
      my_sim.print_bars_file()
      my_sim.print_summary_file()
      my_sim.print_summary_2()

      return redirect('/results1')
  return render_template('form.html', title='Setup', form=form)

@app.route ('/results1')
def results1():
  if not session.get('logged_in'):
    return render_template('no_results.html', title='No hay resultados')

  username = session['username']
  filename = "outputs/"+session['username']+"/pie.csv"
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
  if not session.get('logged_in'):
    return render_template('no_results.html', title='No hay resultados')

  username = session['username']
  filename = "outputs/"+session['username']+"/bars.csv"
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
  if not session.get('logged_in'):
    return render_template('no_results.html', title='No hay resultados')

  username = session['username']
  filenames = []

  filenames.append("outputs/"+session['username']+"/time_evolution_1.csv")
  filenames.append("outputs/"+session['username']+"/time_evolution_2.csv")
  filenames.append("outputs/"+session['username']+"/time_evolution_3.csv")
  filenames.append("outputs/"+session['username']+"/time_evolution_4.csv")
  filenames.append("outputs/"+session['username']+"/time_evolution_5.csv")

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
  if not session.get('logged_in'):
    return render_template('no_results.html', title='No hay resultados')

  username = session['username']
  filename = "outputs/"+session['username']+"/summary.csv"
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
  # app.debug = True # NOT IN PRODUCTION
  app.config.from_object('config')

  app.run()
