Iterations = 100
f = open('output.txt','w')
f.write('active\toff\tstand_by\trepaired_trucks\n')
f.close()

for i in range(Iterations):
    execfile('app.py')

