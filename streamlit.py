#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 15:18:15 2024

@author: alexandre
"""



import streamlit as st
import streamlit.components.v1 as components




st.title('Carte mobilité apprentis')
st.write('Carte des flux de mobilité des apprentis')



@st.cache_data()
def get_map():
  HtmlFile = open("index.html", 'r', encoding='utf-8')
  bcn_map_html = HtmlFile.read()
  return bcn_map_html


bcn_map_html = get_map()


with st.container():
  components.html(bcn_map_html,width=800, height=500)
  
  
