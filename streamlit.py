#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 15:18:15 2024

@author: alexandre
"""



import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import geopandas as gpd


st.set_page_config(layout='wide')

st.title('Carte de mobilité des apprentis')
st.write("Flux entre leur code postal de résidence avant l'apprentissage et celui durant l'apprentissage")


@st.cache_data()

#carte
def get_map():
  HtmlFile = open("index.html", 'r', encoding='utf-8')
  bcn_map_html = HtmlFile.read()
  return bcn_map_html


bcn_map_html = get_map()


#data
data_cp = gpd.read_file('./res/traitement/data_cp.geojson')
data_cp = data_cp[data_cp['apprentis_CP1']!=0]
data_cp = data_cp[['CP', 'Commune', 'apprentis_CP1']]

data_cp = data_cp.sort_values(by=['apprentis_CP1'], ascending=False)
data_cp.reset_index(drop=True, inplace=True)






#mise en page

col1, intercol, col2 = st.columns((3,1,2))


with col1:
    components.html(bcn_map_html,width=780, height=500)
    
    image = Image.open('res/logo_couleur.png')
    st.image(image, width=150)
  


with col2:
    st.dataframe(data_cp, column_config={
        'CP': 'Code postal',
        'DEP': 'Département',
        'Commune': 'Commune',
        'apprentis_CP1': "Nombre total d'apprentis"},
        hide_index=True,
        height=500,
        width=400)
        
    _ = '''
    st.write(pd.read_csv(StringIO(view_csv)))
    '''
    
    
_ = '''
    st.image(view_image, width=800)
    components.iframe(view_url, height=500)
    '''
    
