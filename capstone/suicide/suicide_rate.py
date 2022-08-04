import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px
from scipy import stats

st.set_page_config(layout="wide")

st.title("Kecenderungan Tingkat Bunuh Diri Tinggi di Negara Bahagia")
st.markdown("Capstone Project Tetris DQLab - **Firdhan Hilmy Purnomo**")
st.markdown("---")

#Dataframe definition
df_suic = pd.read_csv('suicide_rate_t.csv', sep=';')
suic_ov = pd.read_csv('suic_overall.csv', sep=';')
df_17 = pd.read_csv('df_17_fix.csv')
df_18 = pd.read_csv('df_18_fix.csv')
df_19 = pd.read_csv('df_19_fix.csv')

#Overview
st.text('"High suicide rates are often cited as evidence of social failure.\nDespite this, some countries and regions that do very well in terms of happiness have among the highest suicide rates."\n(https://voxeu.org/article/suicide-and-happiness)')

st.subheader("Eksplorasi Korelasi")
#
col1,col2 = st.columns([1,4])
with col1:
    year = st.slider('Choose year', 2017, 2018, 2019)
    if year == 2017:
        var_data = df_17
    elif year == 2018:
        var_data = df_18
    elif year == 2019:
        var_data = df_19
    
    num_col = list(var_data.select_dtypes(include=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']))[1:]
    var_x = st.selectbox(
        'Choose Variable X',
        num_col
    )
    var_y = st.selectbox(
        'Choose Variable Y',
        num_col
    )
    st.write("Pearson", round(stats.pearsonr(var_data[var_x], var_data[var_y])[0], 2))


with col2:
    plot = px.scatter(data_frame=var_data, 
                      x=var_x, 
                      y=var_y,
                      trendline='ols',
                      trendline_scope='overall')
    st.plotly_chart(plot)

st.subheader('Kebahagiaan Negara dengan Tingkat Bunuh Diri')
col_kn1, col_kn2, col_kn3, col_kn4 = st.columns([1,2,1,2])
with col_kn1:
    """Dari eksplorasi, dapat diketahui bahwa salah satu pengaruh terbesar 
    dari kebahagiaan suatu negara adalah GDP per Capita. Semakin tinggi
    GDP per Capita sebuah negara, maka Kebahagiaan Negara juga cenderung semakin tinggi."""
with col_kn2:
    happy_gdp = Image.open("happy-gdp.png")
    st.image(happy_gdp, caption = "Korelasi Happy Score dengan GDP per Capita")
with col_kn3:
    """Lalu, bagaimana hubungannya dengan tingkat bunuh diri suatu negara?
    Maka, dapat dilihat korelasinya dengan GDP per Capita karena variabel ini
    yang paling berpengaruh pada kebahagiaan suatu negara. Tidak menggunakan 
    Happy Score karena Happy Score didapatkan dari banyak variabel"""
with col_kn4:
    sc_gdp = Image.open("sc-gdp.png")
    st.image(sc_gdp, caption = "Korelasi Suicide Rate dengan GDP per Capita")

st.subheader('Penutupan')
"""Diantara semua variabel, GDP per Capita memiliki korelasi
tertinggi dengan suicide_rate. Meskipun nilainya tidak besar, 
tapi hal ini bisa memperkuat argumen negara bahagia yang 
penduduknya mayoritas memiliki kekayaan, cenderung memiliki
tingkat bunuh diri yang lebih tinggi"""

st.subheader("Ranked Data")
col_rd1, col_rd2, col_rd3 = st.columns([1,2,2])
with col_rd1:
    conf_suicide = st.selectbox(
        'Pilih Ranked Suicide Rate',
        ['10 Suicide Rate Tertinggi',
        '10 Suicide Rate Terendah',
        'Tertinggi dan Terendah']
    )
    conf_gdp = st.selectbox(
        'Pilih Ranked GDP',
        ['10 GDP Tertinggi',
        '10 GDP Terendah',
        'Tertinggi dan Terendah']
    )
with col_rd2:
    if conf_suicide == '10 Suicide Rate Tertinggi':
        bar1 = px.bar(var_data.iloc[:, 1:].sort_values(by='suicide_rate', ascending=False).head(10),
                      x = 'suicide_rate',
                      y = 'Country',
                      color='Country')
        st.plotly_chart(bar1)
    elif conf_suicide == '10 Suicide Rate Terendah':
        bar1 = px.bar(var_data.iloc[:, 1:].sort_values(by='suicide_rate').head(10),
                      x = 'suicide_rate',
                      y = 'Country',
                      color='Country')
        st.plotly_chart(bar1)
    elif conf_suicide == 'Tertinggi dan Terendah':
        bar1 = px.bar(pd.concat([var_data[var_data.suicide_rate == var_data.suicide_rate.max()],
                      var_data[var_data.suicide_rate == var_data.suicide_rate.min()]]),
                      x = 'suicide_rate',
                      y = 'Country',
                      color='Country')
        st.plotly_chart(bar1)
    
with col_rd3:
    if conf_gdp == '10 GDP Tertinggi':
        bar2 = px.bar(var_data.iloc[:, 1:].sort_values(by='GDP per Capita', ascending=False).head(10),
                      x = 'GDP per Capita',
                      y = 'Country',
                      color='Country')
        st.plotly_chart(bar2)
    elif conf_gdp == '10 GDP Terendah':
        bar2 = px.bar(var_data.iloc[:, 1:].sort_values(by='GDP per Capita').head(10),
                      x = 'GDP per Capita',
                      y = 'Country',
                      color='Country')
        st.plotly_chart(bar2)
    elif conf_gdp == 'Tertinggi dan Terendah':
        bar2 = px.bar(pd.concat([var_data[var_data['GDP per Capita'] == var_data['GDP per Capita'].max()],
                      var_data[var_data['GDP per Capita'] == var_data['GDP per Capita'].min()]]),
                      x = 'GDP per Capita',
                      y = 'Country',
                      color='Country')
        st.plotly_chart(bar2)

st.subheader("Catatan")
"Sumber Data: "
"World Data Bank: https://data.worldbank.org/"
