#!/usr/bin/env python3
import cgitb
import cx_Oracle
import folium
cgitb.enable(format='text')
from jinja2 import Environment, FileSystemLoader

def print_html():
 env = Environment(loader=FileSystemLoader('.'))
 temp = env.get_template('template_1_1.html')
 inpName='Miles'
 inpAge ='25'
 inpOrigin ='Edinburgh'
 inpCastles = castleHtml()
 inpFol = foliumMap()
 print(temp.render(name = inpName, age = inpAge, origin = inpOrigin, castles = inpCastles, map=inpFol))

def castleHtml():
 conn = cx_Oracle.connect("student/train@geoslearn")
 c = conn.cursor()
 c.execute("SELECT * FROM ancient_castles")
 html = ''
 for row in c:
     html = html + row[0] + " which is " + row[1] + " and located in " + row[4] + '<br>'
     conn.close()
     return html

def foliumMap():
 map_l = folium.Map(location=[55.9486,-3.2008], tiles="Stamen Toner", zoom_start=12)
 conn = cx_Oracle.connect("student/train@geoslearn")
 c = conn.cursor()
 c.execute("select castle,LAT_Y,LON_X from ancient_castles")
 for row in c:
     folium.Marker([55.9486,-3.2008],popup='Edinburgh').add_to(map_l)
     conn.close()
     return map_l.get_root().render()

if __name__ == '__main__':
 print_html()
