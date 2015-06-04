import csv


# Open the CSV file for reading
reader = csv.reader(open('data.csv'))

# Create the HTML file for output
htmlfile = open('../templates/table1.html',"w")

# initialize rownum variable
rownum = 0

line = "{%% extends \"base.html\" %%} {%% block content %%} <h1>RESULTADOS 1</h1>"
htmlfile.write(line)

# write <table> tag
htmlfile.write('<table>')

# generate table contents
for row in reader: # Read a single row from the CSV file

  # write header row. assumes first row in csv contains header
  if rownum == 0:
    htmlfile.write('<tr>') # write <tr> tag
      for column in row:
        htmlfile.write('<th>' + column + '</th>')
      htmlfile.write('</tr>')

    #write all other rows 
    else:
      htmlfile.write('<tr>')  
      for column in row:
        htmlfile.write('<td>' + column + '</td>')
      htmlfile.write('</tr>')
  
  #increment row count  
  rownum += 1

# write </table> tag
htmlfile.write('</table>')
htmlfile.write('{%% endblock %%}')
reader.close()
htmlfile.close()