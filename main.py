from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash

from controllers.form import SimForm

app = Flask (__name__)

@app.route ('/')
def home():
  name = 'Tomás'
  return render_template('welcome.html', name=name)

@app.route ('/form', methods=['GET', 'POST'])
def form(): 
  form = SimForm(request.form)
  if request.method == 'POST' and form.validate():
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