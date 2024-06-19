import streamlit as st
import pandas as pd
import numpy as np
import math
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
   # Mapping ranking prosesor ke bobot
   processor_ranking = {
      "AMD Ryzen 9": 100,
      "Intel Core i9": 100,
      "AMD Ryzen 7": 80,
      "Intel Core i7": 60,
      "AMD Ryzen 5": 40,
      "Intel Core i5": 40,
      "Intel Core i3": 20
   }

   # Menambahkan kolom ranking ke dataset
   query['Processor'] = query['Processor'].map(processor_ranking)

   # Mapping ranking VGA ke bobot
   vga_ranking = {
      "NVIDIA RTX4090": 100,
      "NVIDIA RTX4080": 100,
      "NVIDIA RTX4070TI": 100,
      "NVIDIA RTX4070": 100,
      "NVIDIA RTX3080TI": 100,
      "NVIDIA RTX3080": 100,
      "NVIDIA RTX3070TI": 80,
      "NVIDIA RTX3070": 80,
      "NVIDIA RTX3060": 80,
      "NVIDIA RTX4060": 80,
      "NVIDIA RTX3050TI": 80,
      "NVIDIA RTX3050": 80,
      "NVIDIA RTX4050": 60,
      "NVIDIA GTX1660TI": 60,
      "NVIDIA GTX1650": 60,
      "NVIDIA GTX4060": 60,
      "NVIDIA GTX4050": 60,
      "NVIDIA RTX2050": 60,
      "NVIDIA GTX2050": 40,
      "NVIDIA RX6800": 40,
      "NVIDIA RX6800S": 40,
      "NVIDIA RX6700S": 40,
      "NVIDIA RX7600S": 40,
      "NVIDIA MX550": 40,
      "NVIDIA MX530": 20,
      "NVIDIA MX450": 20,
      "NVIDIA MX350": 20,
      "NVIDIA MX330": 20,
      "AMD Radeon": 20,
      "Intel Iris XE": 20
   }

   # Menambahkan kolom ranking ke dataset
   query['VGA'] = query['VGA'].map(vga_ranking)

   def categorize_price(price):
      if price < 10000000:
         return 100
      elif 10000000 <= price < 20000000:
         return 80
      elif 20000000 <= price < 30000000:
         return 60
      elif 30000000 <= price < 40000000:
         return 40
      elif price >= 40000000:
         return 20

   # Terapkan fungsi ke kolom 'harga'
   query['Harga'] = query['Harga'].apply(categorize_price)

   # Mapping ranking prosesor ke bobot
   def categorize_penyimpanan(simpan):
      if simpan == "4TB":
         return 100
      elif simpan == "2TB":
         return 80
      elif simpan == "1TB":
         return 60
      elif simpan == "512GB":
         return 40
      elif simpan == "256GB":
         return 20

   # Terapkan fungsi ke kolom 'harga'
   query['Penyimpanan'] = query['Penyimpanan'].apply(categorize_penyimpanan)

   def categorize_layar(layar):
    if layar == "13 Inch":
        return 20
    elif layar == "14 Inch":
        return 40
    elif layar == "15 Inch":
        return 60
    elif layar == "16 Inch":
        return 80
    elif layar == "17 Inch":
        return 100
    elif layar == "18 Inch":
        return 100

   # Terapkan fungsi ke kolom 'harga'
   query['Ukuran Layar'] = query['Ukuran Layar'].apply(categorize_layar)

   def categorize_keyboard(keyboard):
    if keyboard == "Standart Keyboard":
        return 50
    elif keyboard == "Backlit Keyboard":
        return 100

   # Terapkan fungsi ke kolom 'harga'
   query['Keyboard'] = query['Keyboard'].apply(categorize_keyboard)

   # Mapping ranking prosesor ke bobot
   def categorize_luayara(luayare):
      if luayare == "Non Touchscreen":
         return 50
      elif luayare == "Touchscreen":
         return 100

   # Terapkan fungsi ke kolom 'harga'
   query['Tipe Layar'] = query['Tipe Layar'].apply(categorize_luayara)

   # Mapping ranking prosesor ke bobot
   def categorize_ram(ram):
      if ram == "64GB":
         return 100
      elif ram == "32GB":
         return 80
      elif ram == "16GB":
         return 60
      elif ram == "8GB":
         return 40
      elif ram == "4GB":
         return 20

   # Terapkan fungsi ke kolom 'harga'
   query['RAM'] = query['RAM'].apply(categorize_ram)

   # weigth = {"VGA":0.2,
   #           "Processor":0.2,
   #           "Penyimpanan":0.1,
   #           "Ukuran Layar":0.05,
   #           "RAM":0.2,
   #           "Keyboard":0.05,
   #           "Tipe Layar":0.1,
   #           "Harga":0.1,
   #           }   
   
   matrixNormalitation = []

   # Menghapus kolom nama
   query = query.drop(columns=['Nama'])
   
   # Normalisasi
   def normalization(datacell):
      for column in datacell.columns:
         sum_of_squares = np.sqrt((datacell[column] ** 2).sum())
         # sum_of_squares = ((datacell[column]**2).sum())**(1/2)
         datacell[column] = datacell[column] / sum_of_squares
      return datacell
   
   normalization(query)

   st.html("<h4>Normalisasi</h4>")
   st.dataframe(query)

   # Pembobottan matriks
   weigth = [0.2,0.2,0.1,0.05,0.2,0.05,0.1,0.1] # RxW
   def matrixBoboting(data):
      index = 0
      for column in data.columns:
         data[column] = data[column]*weigth[index]
         index += 1
      return data
   
   matrixBoboting(query)

   st.html("<h4>Pembobotan</h4>")
   st.dataframe(query)

   # Menentukan corcondance dan discordance
   st.html("<h4>Corcondance dan Discordance</h4>")
   def findConcordance(datacell):
      bobot = {
         'VGA':0.2,
         'Processor':0.2,
         'Penyimpanan':0.1,
         'Ukuran Layar':0.05,
         'RAM':0.2,
         'Keyboard':0.05,
         'Tipe Layar':0.1,
         'Harga':0.1,
      }
      concordance = {}
            
      for indeksPrimer in datacell.index.tolist():
         barisPrimer = datacell.loc[indeksPrimer]
         concordance[indeksPrimer] = np.nan
         concordance[indeksPrimer] = {}
         for indeksSekunder in datacell.index.tolist():
            sumKriteria = 0
            barisSekunder = datacell.loc[indeksSekunder]
            for col in datacell.columns:
               if barisPrimer[col] > barisSekunder[col]:
                  sumKriteria = sumKriteria + bobot[col]
               else:
                  sumKriteria = sumKriteria + 0
            concordance[indeksPrimer][indeksSekunder] = sumKriteria 
            
      st.write("Matrix Concordance Table")
      st.dataframe(pd.DataFrame(concordance).transpose())

      return pd.DataFrame(concordance).transpose()
   
   def findDiscordance(datacell):
      bobot = {
         'VGA':0.2,
         'Processor':0.2,
         'Penyimpanan':0.1,
         'Ukuran Layar':0.05,
         'RAM':0.2,
         'Keyboard':0.05,
         'Tipe Layar':0.1,
         'Harga':0.1,
      }
      discordance = {}     
      for indeksPrimer in datacell.index.tolist():
         barisPrimer = datacell.loc[indeksPrimer]
         discordance[indeksPrimer] = np.nan
         discordance[indeksPrimer] = {}
         for indeksSekunder in datacell.index.tolist():
            #seleksi baris sekunder
            barisSekunder = datacell.loc[indeksSekunder]
            #subtract baris primer dengan baris sekunder
            row_subtract = np.subtract(np.array(barisPrimer),np.array(barisSekunder))
            #cari nilai absolute dari nilai tertinggi hasil subtraksi baris
            positif_max = np.abs(row_subtract[np.where(row_subtract > 0, row_subtract, np.inf).argmin()])
            #cari nilai tertinggi negatif dari subtraksi baris, jika tidak ada ganti dengan kode sebelumnnya
            if row_subtract[np.where(row_subtract < 0, row_subtract, -np.inf).argmax()] == 0.0 :
               negatif_max= np.abs(row_subtract[np.where(row_subtract > 0, row_subtract, np.inf).argmin()])
            else:
               negatif_max = np.abs(row_subtract[np.where(row_subtract < 0, row_subtract, -np.inf).argmax()])
            if(math.isnan(np.divide(negatif_max,positif_max)) or np.divide(negatif_max,positif_max) == np.inf):
               discordance[indeksPrimer][indeksSekunder] = 0
            else:
               discordance[indeksPrimer][indeksSekunder] = np.divide(negatif_max,positif_max)
   
      st.write("Matrix Discordance Table")
      st.dataframe(pd.DataFrame(discordance).transpose())     
      
      return pd.DataFrame(discordance).transpose()
   
   queryCor = findConcordance(query)
   queryDis = findDiscordance(query)
      
   # Menentukan Matriks Dominan Corcon dan Disco
   def dominanCor(query):
      st.html("<h4>MATRIKS DOMINAN CORCONDANCE</h4>")
      # nyari threshold
      total_sum = np.sum(query.values)
      m = (query.shape[0])*((query.shape[0])-1)
      findThreshold = total_sum/m

      # buat matriks cornya
      def check_and_replace(value):
         if value > findThreshold:
            return 1
         # elif value == 0:
         #    return "-"
         elif value < findThreshold:
            return 0

      queryMatriksCor = query.applymap(check_and_replace)
      
      st.dataframe(pd.DataFrame(queryMatriksCor))
      return pd.DataFrame(queryMatriksCor)

   def dominanDis(query):
      st.html("<h4>MATRIKS DOMINAN DISCORDANCE</h4>")
      # nyari threshold
      total_sum = np.sum(query.values)
      m = (query.shape[0])*((query.shape[0])-1)
      findThreshold = total_sum/m

      # buat matriks cornya
      def check_and_replace(value):
         if value > findThreshold:
            return 1
         # elif value == 0:
         #    return "-"
         elif value < findThreshold:
            return 0

      queryMatriksDis = query.applymap(check_and_replace)

      st.dataframe(pd.DataFrame(queryMatriksDis))
      return pd.DataFrame(queryMatriksDis)

   queryA = dominanCor(queryCor)
   queryB = dominanDis(queryDis)

   # Menentukan Agregate Dominan Matrix
   def agregate(queryA,queryB):
      st.html("<h4>AGREGATE</h4>")
      agregateQuery = queryA * queryB

      st.dataframe(pd.DataFrame(agregateQuery))
      return pd.DataFrame(agregateQuery)
   
   agregate = agregate(queryA,queryB)

   # perangkingan
   # Menghitung jumlah 1 di setiap baris, kecuali kolom pertama (index)
   agregate['sum_ones'] = agregate.sum(axis=1)

   # Mengurutkan berdasarkan jumlah 1 yang dihitung
   ranking = agregate['sum_ones'].sort_values(ascending=False)

   # Menampilkan hasil ranking
   st.write(ranking)

   final_dataset = df.query('Harga <'+str(st.session_state.budget))
   rank=0
   st.html("<h4>Ranking Final</h4>")
   for indesk in ranking.index.tolist():
      rank=rank+1
      st.write(str(rank) + ". "+ final_dataset.loc[indesk]['Nama'])
