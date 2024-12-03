#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 11:51:20 2024

@author: alexandre
"""



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
import branca.colormap as cm
from branca.element import Template, MacroElement
from IPython.display import IFrame
#from res import legende_html
#from res import format_popup
#from res import bouton_zoom
import base64
import branca
from IPython import get_ipython



#donnees

data_cp = gpd.read_file('res/traitement/data_cp.geojson')

data_flux = pd.read_csv('res/traitement/data_flux.csv', dtype={'code_postal_avant_formation': str,
                                                               'code_postal_apprentissage': str})
data_flux['geom_0'] = shapely.wkt.loads(data_flux['geom_0'])
data_flux['geom_1'] = shapely.wkt.loads(data_flux['geom_1'])



#initialisation carte
my_map = folium.Map(tiles=None, location=[49.862725, 2.287592], zoom_start=8, prefer_canvas=True)
folium.raster_layers.TileLayer(tiles='Cartodb dark_matter', control=False).add_to(my_map)






#couche decoupage codes postaux

popup = folium.GeoJsonPopup(
    fields=['CP', 'Commune'],
    aliases=['Code postal', 'Commune(s)'],
    localize=True,
    sticky=True,
    labels=True,
    style="""
        color: red;
        font-size:12px;
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
    aliases=['Code postal', "Nombre d'apprentis"],
    localize=True,
    sticky=True,
    labels=True,
    style="""
        color: white;
        font-size:12px;
        font-family:Montserrat;
        background-color: #008c95;
        opacity: 0.6;
        border: 1px solid black;
        border-radius: 5px;
        box-shadow: 2px;
        width:200px;
        padding: 5px 1px;
    """
    )



layer_cp = folium.GeoJson(data_cp, style_function=lambda x:{'color': 'grey',
                                                            'weight': 0.6,
                                                            'fillOpacity': 0.5,
                                                            'fillColor': 'darkblue',
                                                            'opacity': 0.4}, 
                          highlight_function = lambda feature:{"color": 'white',
                                                               "weight": 4},
                          popup_keep_highlighted=True,
                          zoom_on_click=False,
                          popup=popup,
                          tooltip=tooltip,
                          name='Codes postaux')
                                                             

layer_cp.add_to(my_map)





#lignes flux
for i in range(len(data_flux)):
    coord_0 = [data_flux['geom_0'][i].y, data_flux['geom_0'][i].x]
    coord_1 = [data_flux['geom_1'][i].y, data_flux['geom_1'][i].x]
    
    poids_cp1 = int(data_flux['nb_tot_apprentis'][i])
    poids_flux = int(data_flux['nombre_personnes'][i])
    
    
    if coord_0 != coord_1:
        
        '''
        flux = folium.PolyLine(
            locations=[coord_0, coord_1],
            color="#59BEC9",
            weight=poids_flux**1.9,
            opacity=np.tanh(poids_flux-0.4)
            )
    
        flux.add_to(my_map)
        
        '''

        
        flux = AntPath(
            locations=[coord_0, coord_1],
            color="#59BEC9",
            pulsecolor='#FF0000',
            weight=int(poids_flux**1.9),
            opacity=np.tanh(poids_flux-0.4),
            dash_array = [1,20],
            delay=5000,
            hardwareAcceleration=True,
            paused=False
            )
        
        flux.add_to(my_map)



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
#fonctionnalite recherche
Search(
    layer=data_com,
    geom_type="Multipolygon",
    placeholder="Rechercher une ville",
    collapsed=False,
    search_label="nom_com",
    weight=3).add_to(my_map)
'''





'''
#formatage de la légende en HTML
legend_html = legende_html.main()
'''


'''
#ajout de la légende à la carte
my_map.get_root().html.add_child(folium.Element(legend_html))
'''



#controle des couches

folium.LayerControl(collapsed=False).add_to(my_map)






'''
#optimiser le niveau de zoom a partir des marqueurs 
list_coord_lat = [coord[0] for coord in list_points]
list_coord_long = [coord[1] for coord in list_points]
dic_coord = {'lat': list_coord_lat, 'long': list_coord_long}
df_coord = pd.DataFrame(dic_coord)


min_coord_points = df_coord.min().values.tolist()
max_coord_points = df_coord.max().values.tolist()

my_map.fit_bounds([min_coord_points, max_coord_points])

'''





#logo LARIIS
logo_lariis = 'res/logo_noir.png'
FloatImage(logo_lariis, bottom=1, left=1, width='100px').add_to(my_map)



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