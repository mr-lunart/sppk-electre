import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv('kliknklik_gaming_laptop_cleaned.csv')

# columns_to_drop = ['Garansi', 'Warna', 'Microsoft Office','Dimensi','Berat']
# columns_to_drop = [col for col in columns_to_drop if col in df.columns]
# data = df.drop(columns_to_drop, axis=1)

# st.dataframe(df)

for harga in df['Harga']:
   harga = "test"
   st.write(harga)

with st.form("my_form"):
   st.text_input("VGA", key="vga")
   st.text_input("Proccessor", key="proc")
   st.text_input("Penyimpanan", key="storage")
   st.text_input("Ram", key="ram")
   st.text_input("Tipe Penyimpanan", key="storageType")
   st.text_input("Tipe Layar", key="screen")
   st.text_input("Ukuran Layar", key="screenSize")
   st.text_input("Warna", key="color")
   st.text_input("Sistem Operasi", key="sistem")
   st.form_submit_button('Submit')

st.write()