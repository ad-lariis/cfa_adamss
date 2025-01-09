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
import tableauserverclient as TSC
import jwt
import datetime
import uuid
import requests
from io import StringIO
from pathlib import Path




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





#tableau
tableau_auth = TSC.PersonalAccessTokenAuth(
    st.secrets["tableau"]["token_name"],
    st.secrets["tableau"]["token_secret"],
    st.secrets["tableau"]["site_id"],
)
server = TSC.Server(st.secrets["tableau"]["server_url"], use_server_version=True)



with server.auth.sign_in(tableau_auth):
    all_workbooks = list(TSC.Pager(server.workbooks))
    
    list_name = [wb.name for wb in all_workbooks]
    list_id = [wb.id for wb in all_workbooks]
    
    dic_wb = dict(zip(list_name, list_id))
    
    #dic de corresp entre le nom et l'id du workbook
    wb_cfa_id = dic_wb['cfa adamss']
    workbook_cfa = server.workbooks.get_by_id(wb_cfa_id)
    
    server.workbooks.populate_views(workbook_cfa)
    list_views = [view.name for view in workbook_cfa.views]
    view_item = workbook_cfa.views[3]
    _ = '''
    server.views.populate_image(view_item)
    view_image = view_item.image
    view_url = view_item.content_url
    '''
    server.views.populate_csv(view_item)
    view_csv = b"".join(view_item.csv).decode("utf-8")






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
    
