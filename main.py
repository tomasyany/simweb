from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from controllers.form import SimForm

app = Flask (__name__)

@app.route ('/')
def home():
  name = 'Tomás'
  return render_template('welcome.html', name=name)

@app.route ('/form', methods=['GET', 'POST'])
def form(): 
  form = SimForm()
  if form.validate_on_submit(): 
    return redirect('/results1')
  return render_template('form.html', title='Formulario', form=form)


@app.route ('/results1')
def results1(): 
  return render_template('results1.html', title='Resultados 1')

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