#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 11:51:20 2024

@author: alexandre
"""



import os

import folium
from folium.features import DivIcon
from folium.plugins import FloatImage
from folium.plugins import Search
from folium.plugins import AntPath
import webbrowser
from folium.plugins import MarkerCluster
import pandas as pd
import numpy as np
import geopandas as gpd
import shapely.wkt
import json
import random
from branca.colormap import linear
from branca.element import Template, MacroElement
from IPython.display import IFrame
from PIL import Image
#from res import legende_html
#from res import format_popup
#from res import bouton_zoom
import base64
import branca
from IPython import get_ipython
from pathlib import Path



#donnees

data_cp = gpd.read_file('res/traitement/data_cp.geojson')

data_flux = pd.read_csv('res/traitement/data_flux.csv', dtype={'code_postal_avant_formation': str,
                                                               'code_postal_apprentissage': str})
data_flux['geom_0'] = shapely.wkt.loads(data_flux['geom_0'])
data_flux['geom_1'] = shapely.wkt.loads(data_flux['geom_1'])



#initialisation carte
my_map = folium.Map(tiles=None, location=[50.362725, 2.287592], zoom_start=7.5, prefer_canvas=True)
folium.raster_layers.TileLayer(tiles='Cartodb dark_matter', control=False).add_to(my_map)






#couche decoupage codes postaux

popup = folium.GeoJsonPopup(
    fields=['CP', 'Commune'],
    aliases=['Code postal', 'Commune(s)'],
    localize=True,
    sticky=True,
    labels=True,
    style="""
        color: white;
        font-size:10px;
        font-family:Montserrat;
        background-color: #008c95;
        opacity: 0.6;
        border: 1px solid black;
        border-radius: 5px;
        box-shadow: 2px;
        width:300px;
        white-space: pre-wrap;
    """
    )




tooltip = folium.GeoJsonTooltip(
    fields=['CP', 'apprentis_CP1'],
    aliases=['Code postal', "Nb d'apprentis"],
    localize=True,
    sticky=True,
    labels=True,
    style="""
        color: white;
        font-size:10px;
        font-family:Montserrat;
        background-color: #008c95;
        opacity: 0.6;
        border: 1px solid black;
        border-radius: 5px;
        box-shadow: 2px;
        width:120px;
        padding: 5px 1px;
    """
    )



data = data_cp
data.reset_index(drop=True, inplace=True)

cm = branca.colormap.StepColormap(['darkblue', 'lightgray', 'orange', 'red'], vmin=0, vmax=20, index=[0,1,4,8,20])
cm = cm.to_linear()
cm.caption = "Nombre d'apprentis"


layer_cp = folium.GeoJson(data, style_function=lambda x:{'color': 'grey',
                                                         'weight': 0.6,
                                                         'opacity': 0.4,
                                                         'fillColor': cm(x['properties']['apprentis_CP1']),
                                                         'fillOpacity': 0.5}, 
                          
                          highlight_function = lambda feature:{"color": 'white',
                                                               "weight": 3},
                          popup_keep_highlighted=True,
                          zoom_on_click=False,
                          popup=popup,
                          tooltip=tooltip,
                          overlay=False,
                          name='Codes postaux')
                                                             

layer_cp.add_to(my_map)


#ajout de la colormap a la carte
#cm.add_to(my_map)





'''

#couche loyer T1 et T2 par commune en 2023 dans la region HDF
data_loyer = gpd.read_file('res/loyer/data_loyer_hdf.geojson')



popup = folium.GeoJsonPopup(
    fields=['LIBGEO', 'loypredm2'],
    aliases=['Commune', 'Loyer'],
    localize=True,
    sticky=True,
    labels=True,
    style="""
        color: white;
        font-size:10px;
        font-family:Montserrat;
        background-color: #008c95;
        opacity: 0.6;
        border: 1px solid black;
        border-radius: 5px;
        box-shadow: 2px;
        width:300px;
        white-space: pre-wrap;
    """
    )




tooltip = folium.GeoJsonTooltip(
    fields=['LIBGEO'],
    aliases=['Commune'],
    localize=True,
    sticky=True,
    labels=True,
    style="""
        color: white;
        font-size:10px;
        font-family:Montserrat;
        background-color: #008c95;
        opacity: 0.6;
        border: 1px solid black;
        border-radius: 5px;
        box-shadow: 2px;
        width:120px;
        padding: 5px 1px;
    """
    )



layer_loyer = folium.Choropleth(geo_data=data_loyer.to_json(), data=data_loyer[['INSEE_C', 'LIBGEO', 'loypredm2']], columns=['INSEE_C', 'LIBGEO', 'loypredm2'],
                                fill_color='Greens', key_on='feature.properties.INSEE_C',
                                overlay=True,
                                control=True,
                                show=False,
                                name='Loyer')


                                                            
                                                             

layer_loyer.add_to(my_map)

'''




#lignes flux
for i in range(len(data_flux)):
    coord_0 = [data_flux['geom_0'][i].y, data_flux['geom_0'][i].x]
    coord_1 = [data_flux['geom_1'][i].y, data_flux['geom_1'][i].x]
    
    poids_cp1 = int(data_flux['nb_tot_apprentis'][i])
    poids_flux = int(data_flux['nombre_personnes'][i])
    
    
    if coord_0 != coord_1:

        
        flux = AntPath(
            locations=[coord_0, coord_1],
            color="#59BEC9",
            pulsecolor='#FF0000',
            weight=int(poids_flux**1.9),
            opacity=np.tanh(poids_flux-0.4),
            dash_array = [1,20],
            delay=1000,
            hardwareAcceleration=True,
            paused=False
            )
        
        flux.add_to(my_map)


'''
    #cercles communes CP
    folium.CircleMarker(
        location=coord_1,
        radius=poids_flux**1.5,
        fill=True,
        fill_opacity=0.5,
        opacity=0.6,
        color='#CCA1A6'
        ).add_to(my_map)
'''



#controle des couches

folium.LayerControl(collapsed=False).add_to(my_map)





#logo LARIIS
path = Path.cwd()
logo_lariis_path = path / 'res/logo_couleur.png'

with open(logo_lariis_path, 'rb') as lf:
  # open in binary mode, read bytes, encode, decode obtained bytes as utf-8 string
  b64_content = base64.b64encode(lf.read()).decode('utf-8')

FloatImage('data:image/png;base64,{}'.format(b64_content), bottom=1, left=1, width='100px').add_to(my_map)



html_to_insert = "<style>.leaflet-popup-content-wrapper, .leaflet-popup.tip {background-color: #008c95 !important; }</style>"

my_map.get_root().header.add_child(folium.Element(html_to_insert))






#supprime le rectangle qui s'affiche au click sur Google Chrome


'''
get_ipython().run_cell_magic('javascript', '',
    f"var map = document.getElementById('{map_id}');"
    f"var style = document.createElement('style');"
    f"style.innerHTML = 'path.leaflet-interactive:focus {{ outline: none; }}';"
    f"map.appendChild(style);"
    f".leaflet-interactive.selected {{ outline: none; }}"
)
'''




#export en html
my_map.save("index.html")