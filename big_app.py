Iterations = 10
f = open('data.csv', 'w')
f.write('Tiempo activo,Tiempo en taller,Tiempo en stand-by,'
        'Vehiculos reparados\n')
f.close()

for i in range(Iterations):
    execfile('app.py')

