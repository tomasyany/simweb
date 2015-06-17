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

      # l1 = [["exponential",[10]], ["exponential", [10]]]
      l2 = [["poisson", [0.3]], ["poisson", [0.3]]]
      # my_sim = Simulation(60,5,2,1,2,["qw", "as"],l2,l2,l2,[1, 1],600)
      # my_sim = Simulation(30,3,2,2,2,["c1", "c2"],l2,l2,l2,[1, 1], 365)
      # print(replications, total_trucks, design_number,
      #            workshop_capacity, n_components, comp_names,
      #            life_dist_parameters, repair_dist_parameters,
      #            replacement_dist_parameters, start_inventory,
      #            simulation_horizon)

      # my_sim = Simulation(replications, total_trucks, design_number,
      #            workshop_capacity, n_components, comp_names,
      #            life_dist_parameters, repair_dist_parameters,
      #            replacement_dist_parameters, start_inventory,
      #            simulation_horizon)
      my_sim.run_simulation()
      
      return redirect('/results1')
  return render_template('form.html', title='Setup', form=form)

@app.route ('/results1')
def results1():
  return render_template('results1.html', title='Resultados 1')

@app.route ('/table1')
def table1(): 
  return render_template('table1.html', title='Resultados 1')

@app.route ('/results2')
def results2(): pass

@app.route ('/results3')
def results3(): pass

@app.route ('/download')
def download(): pass



if __name__ == "__main__":
  app.debug = True # NOT IN PRODUCTION
  app.config.from_object('config')

  app.run()