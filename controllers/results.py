import csv


# Open the CSV file for reading
reader = csv.reader(open('data.csv'))

# Create the HTML file for output
htmlfile = open('../templates/results1.html',"w")

# initialize rownum variable
rownum = 0



my_script = open('script.txt', 'r')

line = "{% extends \"base.html\" %} {% block content %}"
htmlfile.write(line)



line = "<h1 style=\"text-align:center\">RESULTADOS</h1>"
htmlfile.write(line)

# write <table> tag
htmlfile.write('<table class=\"table table-striped\">')

promedio = [0,0,0]

titulos = []
# generate table contents
for row in reader: # Read a single row from the CSV file

  # write header row. assumes first row in csv contains header
  if rownum == 0:
    htmlfile.write('<tr>') # write <tr> tag
    for column in row:
      titulos.append(column)
      htmlfile.write('<th>' + column + '</th>')
    htmlfile.write('</tr>')

  #write all other rows 
  else:
    htmlfile.write('<tr>') 
    columnNum=0
    for column in row:
      if columnNum == 0:
        promedio[0] += float(column)
      elif columnNum == 1:
        promedio[1] += float(column)
      elif columnNum == 2:
        promedio[2] += float(column)

      if(float(column)<1):
        column = "{0:.0f}%".format(float(column) * 100)
      htmlfile.write('<td>' + column + '</td>')
      columnNum += 1
    htmlfile.write('</tr>')
  
  #increment row count  
  rownum += 1

for i in range(0,len(promedio)):
  promedio[i] = float(promedio[i]/(rownum-1))


# write </table> tag
htmlfile.write('</table>')

lines = my_script.readlines()
for line in lines:
  htmlfile.write(line)



line = 'var data = google.visualization.arrayToDataTable(['
htmlfile.write(line)
line = "[\'Tiempo\', \'Porcentaje\'],"

htmlfile.write(line)
line=""
for i,titulo in enumerate(titulos[:3]):
  line += '[\''+ titulo + '\',' + str(promedio[i]) + '],'

line += ']);'
htmlfile.write(line)

my_script.close()

my_script = open('script2.txt', 'r')
lines = my_script.readlines()
for line in lines:
  htmlfile.write(line)

my_script.close()

line = "</script>"
htmlfile.write(line)

    
htmlfile.write('<div  id=\"piechart\" style=\"width: 50%; height: 500px; margin: 0 auto;\"></div>')

htmlfile.write('{% endblock %}')
htmlfile.close()