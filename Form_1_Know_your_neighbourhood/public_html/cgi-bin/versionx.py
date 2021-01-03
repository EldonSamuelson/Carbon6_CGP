#!/usr/bin/env python3
import cx_Oracle
import cgi
import cgitb
from jinja2 import Environment, FileSystemLoader
cgitb.enable(format='text/html')

with open("../../oracle",'r') as pwf:
    pw = pwf.read().strip()
    
# Create instance of FieldStorage
form = cgi.FieldStorage()

mylist1=[]
mylist2=[]
mylist3=[]
mylist4=[]
x=0

# Get data from radiobutton 

if form.getvalue('Radiochoice'):
   user_choice = form.getvalue('Radiochoice')
else:
   pass

# Get data from Zones Form 2
if form.getvalue('Zones_Multicombo'):
    subject = form.getvalue('Zones_Multicombo')
    # checks if a user selects single choice
    if (type(subject))==str:
        mylist1.append(int(subject))
    # if a user selects multiple choices (subject will then belong to a datatype like tuple/list) 
    else:
        for row in subject[0 : : 1]:
            mylist1.append(row) 
else:
   subject = "Not entered"
   pass
   
conn = cx_Oracle.connect(dsn="geoslearn",user="s1624036",password=pw)
c = conn.cursor()
# checking for radio button choices
if user_choice=='Demographic':
    c.execute("SELECT ZONENAME, EDIRANK, AREAHA, POP, POPPERHA FROM EDI")
    for row in c:
        mylist2.append(row)
    fields=("ZONE NAME", "EDI RANK", "AREA (ha)", "POPULATION", "POPULATION DENSITY")
    conn.close
elif user_choice=='Environmental':
    c.execute("SELECT ZONENAME, EDIRANK, TREECOUNT, TREESPERHA, MEANDBH, JUVCOUNT, JUVPERHA, SPECIES, SPECIESPERTREE FROM EDI")
    for row in c:
        mylist2.append(row) 
    fields=("ZONE NAME", "EDI RANK", "TOTAL TREE COUNT", "TREES (PER ha)", "MEAN DBH (cm)", "JUVENILE TREE COUNT", "JUVENILE TREES (PER ha)", "TOTAL TREE SPECIE COUNT", "TREE SPECIES (PER ha)")
    conn.close
elif user_choice=='Tree_Percentage':
    c.execute("SELECT ZONENAME, EDIRANK, PERCHIGH, PERCMED, NFIPERC FROM EDI")
    for row in c:
        mylist2.append(row) 
    fields=("ZONE NAME", "EDI RANK", "DENSE TREES", "SCATTERED TREES", "WOODLAND COVER")
    conn.close   
elif user_choice=='Tree_Hectare':
    c.execute("SELECT ZONENAME, EDIRANK, HIGHHA, MEDHA, NFIHA FROM EDI")
    for row in c:
        mylist2.append(row) 
    fields=("ZONE NAME", "EDI RANK", "DENSE TREES", "SCATTERED TREES", "WOODLAND COVER")
    conn.close
else:
    conn.close
    pass

for i in mylist1:
    mylist3.append(mylist2[int(i)-1])
        
def print_html():
        env = Environment(loader=FileSystemLoader('.'))
        temp = env.get_template('versionx.html')
        inpEDI=mylist3
        inpHeading=fields
        print(temp.render(heading = inpHeading, data=inpEDI)) 

if __name__ == '__main__':
	print_html()