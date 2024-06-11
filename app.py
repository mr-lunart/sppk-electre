import streamlit as st
import pandas as pd
import numpy as np
df = pd.read_csv('kliknklik_gaming_laptop_cleaned.csv')

def set_analisa():
   st.session_state['analisa'] = True

if 'analisa' not in st.session_state:
    st.session_state['analisa'] = False

st.title("ELECTRE SISTEM V0.1")
st.html('<h3>Input Budget</h3>')
with st.form("my_form"):
   budget = st.text_input("Budget", key="budget",)
   submit = st.form_submit_button('Submit')
   
st.divider()

if submit == True:
   query = df.query('Harga <'+str(budget))
   st.dataframe(query)
   st.button('Analisa',key='analisa',on_click = set_analisa)

if st.session_state.analisa == True:
   st.html('<h3>Analisa ELECTRE</h3>')
   query = df.query('Harga <'+str(st.session_state.budget))
   st.dataframe(query)



