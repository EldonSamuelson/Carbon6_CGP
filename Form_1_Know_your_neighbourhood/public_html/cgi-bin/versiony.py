#!/usr/bin/python

# Import modules for CGI handling
import folium
import cgi
import cgitb
import json

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
if form.getvalue('EDI_Combo'):
   edi = form.getvalue('EDI_Combo')
else:
   edi = "Not entered"

print ("Content-type:text/html\r\n\r\n")
print ("<html>")
print ("<head>")
print ("<title>EDI Form Output</title>")
print ("</head>")
print ("<body>")

m = folium.Map(location=[55.9400,-3.2000],zoom_start=11,tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',attr='OpenStreetMap')
stylex = {'fillColor': '#F08080', 'color': '#F08080', 'weight':0.5, 'fillOpacity' : 0.0}
geojsonx = 'edizones.geojson'
g = folium.GeoJson(
    geojsonx,
    name='geojsonx',style_function=lambda x:stylex
).add_to(m)

# Checking User Values, for rendering polygons correspnding to each EDI 

if int(edi)==10:
    geojson10 = 'edi10.geojson'
    style2 = {'fillColor': '#9FE2BF', 'color': '#40E0D0', 'weight':1.0, 'fillOpacity' : 0.5}
    h = folium.GeoJson(
    geojson10,
    name='geojson10',style_function=lambda x:style2
    ).add_to(m)
    folium.GeoJsonTooltip(fields=["Name","EDIRANK"]).add_to(h)
    print (m.get_root().render())
   
elif int(edi)==9:
    geojson9 = 'edi9.geojson'
    style3 = {'fillColor': '#9FE2BF', 'color': '#40E0D0', 'weight':1.0, 'fillOpacity' : 0.5}
    h = folium.GeoJson(
    geojson9,
    name='geojson9',style_function=lambda x:style3
    ).add_to(m)
    folium.GeoJsonTooltip(fields=["Name","EDIRANK"]).add_to(h)
    print (m.get_root().render())

elif int(edi)==8:
    geojson8 = 'edi8.geojson'
    style4 = {'fillColor': '#9FE2BF', 'color': '#40E0D0', 'weight':1.0, 'fillOpacity' : 0.5}
    h = folium.GeoJson(
    geojson8,
    name='geojson8',style_function=lambda x:style4
    ).add_to(m)
    folium.GeoJsonTooltip(fields=["Name","EDIRANK"]).add_to(h)
    print (m.get_root().render())

elif int(edi)==7:
    geojson7 = 'edi7.geojson'
    style5 = {'fillColor': '#9FE2BF', 'color': '#40E0D0', 'weight':1.0, 'fillOpacity' : 0.5}
    h = folium.GeoJson(
    geojson7,
    name='geojson7',style_function=lambda x:style5
    ).add_to(m)
    folium.GeoJsonTooltip(fields=["Name","EDIRANK"]).add_to(h)
    print (m.get_root().render())

elif int(edi)==6:
    geojson6 = 'edi6.geojson'
    style6 = {'fillColor': '#9FE2BF', 'color': '#40E0D0', 'weight':1.0, 'fillOpacity' : 0.5}
    h = folium.GeoJson(
    geojson6,
    name='geojson6',style_function=lambda x:style6
    ).add_to(m)
    folium.GeoJsonTooltip(fields=["Name","EDIRANK"]).add_to(h)
    print (m.get_root().render())
    
elif int(edi)==5:
    geojson5 = 'edi5.geojson'
    style5 = {'fillColor': '#9FE2BF', 'color': '#40E0D0', 'weight':1.0, 'fillOpacity' : 0.5}
    h = folium.GeoJson(
    geojson5,
    name='geojson5',style_function=lambda x:style5
    ).add_to(m)
    folium.GeoJsonTooltip(fields=["Name","EDIRANK"]).add_to(h)
    print (m.get_root().render())
    
elif int(edi)==4:
    geojson4 = 'edi4.geojson'
    style4 = {'fillColor': '#9FE2BF', 'color': '#40E0D0', 'weight':1.0, 'fillOpacity' : 0.5}
    h = folium.GeoJson(
    geojson4,
    name='geojson4',style_function=lambda x:style4
    ).add_to(m)
    folium.GeoJsonTooltip(fields=["Name","EDIRANK"]).add_to(h)
    print (m.get_root().render())
    
elif int(edi)==3:
    geojson3 = 'edi3.geojson'
    style3 = {'fillColor': '#9FE2BF', 'color': '#40E0D0', 'weight':1.0, 'fillOpacity' : 0.5}
    h = folium.GeoJson(
    geojson3,
    name='geojson3',style_function=lambda x:style3
    ).add_to(m)
    folium.GeoJsonTooltip(fields=["Name","EDIRANK"]).add_to(h)
    print (m.get_root().render())    

elif int(edi)==2:
    geojson2 = 'edi2.geojson'
    style2 = {'fillColor': '#9FE2BF', 'color': '#40E0D0', 'weight':1.0, 'fillOpacity' : 0.5}
    h = folium.GeoJson(
    geojson2,
    name='geojson2',style_function=lambda x:style2
    ).add_to(m)
    folium.GeoJsonTooltip(fields=["Name","EDIRANK"]).add_to(h)
    print (m.get_root().render())
    
elif int(edi)==1:
    geojson1 = 'edi1.geojson'
    style1 = {'fillColor': '#9FE2BF', 'color': '#40E0D0', 'weight':1.0, 'fillOpacity' : 0.5}
    h = folium.GeoJson(
    geojson1,
    name='geojson1',style_function=lambda x:style1
    ).add_to(m)
    folium.GeoJsonTooltip(fields=["Name","EDIRANK"]).add_to(h)
    print (m.get_root().render())
    
elif int(edi)==0:
    geojson0 = 'edi0.geojson'
    style0 = {'fillColor': '#9FE2BF', 'color': '#40E0D0', 'weight':1.0, 'fillOpacity' : 0.5}
    h = folium.GeoJson(
    geojson0,
    name='geojson0',style_function=lambda x:style0
    ).add_to(m)
    folium.GeoJsonTooltip(fields=["Name","EDIRANK"]).add_to(h)
    print (m.get_root().render())
    
else:
    pass
    
print ("</body>")
print ("</html>")
