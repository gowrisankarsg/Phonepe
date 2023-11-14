import pandas as pd
import os
import json
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu

import aggregatted, map, top

st.set_page_config(
        page_title="Phonepe_pulse",
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='Phonepe_pulse ',
                options=['Aggregatted','Map','Top'],
                icons=['house-fill','person-circle','trophy-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )

        st.title("Phonepe Pulse Data Visualization and Exploration")

        if app == "Aggregatted":
            aggregatted.aggtrans()
        if app == "Map":
            map.maptrans()
        if app == "Top":
            top.toptrans()
           
             
          
             
    run() 







