#import section
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import streamlit as st
import datetime
import os

sns.set(style='dark')

def tren_pm25(df):
    st.subheader("Tren Kualitas Udara Berdasarkan PM2.5 di tiap Station")
    particle_df = df.groupby(by=["station", "year"]).agg({
        "PM2.5": "mean",
        "PM10": "mean"
    }).reset_index()

    particle_df['year'] = particle_df['year'].astype(str)

    # Membuat figure baru
    plt.figure(figsize=(20, 10))
    sns.lineplot(x='year', y='PM2.5', hue='station', data=particle_df, marker='o')

    plt.title('Rata-rata PM2.5 per Stasiun dan Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata PM2.5')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(plt.gcf())

def compare_pm25(df):
    st.subheader("Perbandingan Kualitas Udara Berdasarkan PM2.5 untuk yang Terbaik dan Terburuk")
    #mendapatkan mean dengan station
    temp_df = df.groupby(by=["station"]).agg({
        "PM2.5": "mean",
        "PM10": "mean"
    }).reset_index()

    #mendapatkan min dan max mean per station
    min_pm25 = temp_df[temp_df['PM2.5'] == temp_df['PM2.5'].min()].reset_index().station[0]
    max_pm25 = temp_df[temp_df['PM2.5'] == temp_df['PM2.5'].max()].reset_index().station[0]

    #select baris berdasarkan min dan max diatas pada dataframe yang ada year nya
    temp_station_year_pm25_df = df.groupby(by=["station", "year"]).agg({
        "PM2.5": "mean",
    }).reset_index()

    temp_station_year_pm25_df['year'] = temp_station_year_pm25_df['year'].astype(str)

    min_n_max_pm25_df = temp_station_year_pm25_df[(temp_station_year_pm25_df['station'] == min_pm25) | (temp_station_year_pm25_df['station'] == max_pm25)]

    # Membuat figure baru
    plt.figure(figsize=(20, 10))
    sns.lineplot(x='year', y='PM2.5', hue='station', data=min_n_max_pm25_df, marker='o')

    plt.title('Rata-rata PM2.5 per Stasiun dan Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata PM2.5')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    st.pyplot(plt.gcf())

def tren_pm10(df):
    st.subheader("Tren Kualitas Udara Berdasarkan PM10 di tiap Station")
    particle_df = df.groupby(by=["station", "year"]).agg({
        "PM2.5": "mean",
        "PM10": "mean"
    }).reset_index()

    particle_df['year'] = particle_df['year'].astype(str)

    # Membuat figure baru
    plt.figure(figsize=(20, 10))
    sns.lineplot(x='year', y='PM10', hue='station', data=particle_df, marker='o')
    plt.title('Rata-rata PM10 per Stasiun dan Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata PM10')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(plt.gcf())

def compare_pm10(df):
    st.subheader("Perbandingan Kualitas Udara Berdasarkan PM10 untuk yang Terbaik dan Terburuk")
    #mendapatkan mean dengan station
    temp_df = df.groupby(by=["station"]).agg({
        "PM2.5": "mean",
        "PM10": "mean"
    }).reset_index()

    #mendapatkan min dan max mean per station
    min_pm10 = temp_df[temp_df['PM10'] == temp_df['PM10'].min()].reset_index().station[0]
    max_pm10 = temp_df[temp_df['PM10'] == temp_df['PM10'].max()].reset_index().station[0]

    #select baris berdasarkan min dan max diatas pada dataframe yang ada year nya
    temp_station_year_pm10_df = df.groupby(by=["station", "year"]).agg({
        "PM10": "mean",
    }).reset_index()
    temp_station_year_pm10_df['year'] = temp_station_year_pm10_df['year'].astype(str)

    min_n_max_pm10_df = temp_station_year_pm10_df[(temp_station_year_pm10_df['station'] == min_pm10) | (temp_station_year_pm10_df['station'] == max_pm10)]

    # Membuat figure baru
    plt.figure(figsize=(20, 10))
    sns.lineplot(x='year', y='PM10', hue='station', data=min_n_max_pm10_df, marker='o')

    plt.title('Rata-rata PM10 per Stasiun dan Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata PM10')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    st.pyplot(plt.gcf())

def pollutan_gases_df(df):
    newdf = df.groupby(by=["station", "year"]).agg({
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
    }).reset_index()

    newdf['year'] = newdf['year'].astype(str)
    return newdf

def corr_ozon(df):
    corr_polution = df.groupby(by=["station"]).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
    }).corr()

    plt.figure(figsize=(20, 10))
    sns.heatmap(corr_polution, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
    plt.title('Heatmap Korelasi antara O3 dan Polutan Lainnya')
    st.pyplot(plt.gcf())

def corr_all_weather(df):
    corr_weather = df[['TEMP', 'PRES', 'DEWP', 'RAIN', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr()

    plt.figure(figsize=(20, 10))
    sns.heatmap(corr_weather, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
    plt.title('Heatmap Korelasi antara Cuaca Terhadap Kualitas Udara')
    st.pyplot(plt.gcf())

def mata_angin(df):
    #first declaration
    st.markdown("Ploting pada Peta")
    filtered_station_df = df.groupby('station').agg({
        'PM2.5': 'mean',
        'wd': lambda x: x.mode().iat[0] if len(x.mode()) > 0 else None,  # Mengatasi multiple modes
        'long': lambda x: x.mode().iat[0],
        'lat': lambda x: x.mode().iat[0],
    }).reset_index()

    filtered_gdf = gpd.GeoDataFrame(filtered_station_df, geometry=gpd.points_from_xy(filtered_station_df.long, filtered_station_df.lat))

    # Plot peta dengan stasiun
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    ax = world.plot(figsize=(20, 10))
    filtered_gdf.plot(ax=ax, column='station', marker='o', markersize=25, cmap='tab20', legend=True, categorical=True)
    plt.title('Peta Stasiun Pengukuran Kualitas Udara')

    plt.xlim(115, 118)
    plt.ylim(38, 42)
    st.pyplot(plt.gcf())

    #second using arrow
    st.subheader("Visualisasi Arah Mata Angin")
    ax = world.plot(figsize=(20, 10))
    filtered_gdf.plot(ax=ax, column='station', marker='o', markersize=25, cmap='tab20', legend=True, categorical=True)

    # Konversi arah angin ke derajat
    wind_directions = {
        'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
        'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
        'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
        'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
    }

    # Fungsi untuk membuat panah berdasarkan arah angin
    def arrow(x):
        angle_deg = wind_directions.get(x, 0)  # Menggunakan 0 jika arah angin tidak terdaftar
        angle_rad = np.radians(angle_deg)
        return 0.1 * np.cos(angle_rad), 0.1 * np.sin(angle_rad)

    # Menambahkan panah untuk setiap stasiun
    for i, row in filtered_station_df.iterrows():
        ax.arrow(row['long'], row['lat'], *arrow(row['wd']), head_width=0.1, head_length=0.02, fc='red')

    plt.title('Peta Stasiun dengan Arah Angin')
    plt.xlim(115, 118)
    plt.ylim(39.5, 41)
    st.pyplot(plt.gcf())

    #third clustering
    st.subheader("Clustering Berdasarkan Arah Mata Angin")
    clusters = []
    for wd, group in filtered_gdf.groupby('wd'):
        clusters.append(group)

    # Tampilkan hasil clustering
    for i, cluster in enumerate(clusters):
        print(f'Cluster {i+1}: {len(cluster)} stasiun')
        print(cluster)
        
    # Plot peta dengan stasiun yang diwarnai berdasarkan cluster
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    ax = world.plot(figsize=(20, 10))

    # Plot stasiun dalam setiap cluster dengan warna berbeda
    colors = ['red', 'green', 'blue', 'purple', 'orange', 'yellow']
    for i, cluster in enumerate(clusters):
        cluster.plot(ax=ax, marker='o', markersize=70, color=colors[i % len(colors)], label=cluster['wd'].iloc[0])
        
    for i, row in filtered_station_df.iterrows():
        ax.arrow(row['long'], row['lat'], *arrow(row['wd']), head_width=0.1, head_length=0.02, fc='red')

    plt.title('Peta Stasiun dengan Arah Angin')
    plt.xlim(115, 118)
    plt.ylim(39.5, 41)
    plt.legend()
    st.pyplot(plt.gcf())

    #fourth compare with some pollutan
    st.subheader("Perbandingan Antara Arah Mata Angin dengan Polutan PM2.5")
    clustered_df = pd.concat(clusters)
    grouped_cluster_df = clustered_df.groupby(by=["wd"]).agg({
        'PM2.5': 'mean'
    })

    grouped_cluster_df = grouped_cluster_df.sort_values(by='PM2.5', ascending=True)

    grouped_cluster_df.plot(kind='barh', legend=False)
    plt.title('Rata-rata PM2.5 berdasarkan Arah Angin')
    plt.ylabel('Arah Angin')
    plt.xlabel('Rata-rata PM2.5')
    st.pyplot(plt.gcf())

    st.subheader('Table Arah Mata Angin dan Station dengan Polutan PM2.5')
    clustered_df = clustered_df.groupby(by=["wd", "station"]).agg({
        'PM2.5': 'mean'
    }).reset_index()
    st.dataframe(clustered_df)

# Mendapatkan path file main_data.csv
file_path = os.path.join("dashboard", "main_data.csv")

df = pd.read_csv(file_path)
min_year = df['year'].min()
max_year = df['year'].max()

min_date = datetime.date(min_year, 1, 1)
max_date = datetime.date(max_year, 12, 31)

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
str_start_date = str(start_date).split('-')[0]
str_end_date = str(end_date).split('-')[0]

main_df = df[(df["year"] >= int(str_start_date)) & (df["year"] <= int(str_end_date))]

st.header('Dashboard Kualitas udara')
st.subheader('Tren Kualitas Udara dalam tahun {} - {}'.format(str_start_date, str_end_date), divider='rainbow')

#question 1
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"])

with tab1:
    tren_pm25(main_df)
    compare_pm25(main_df)

with tab2:
    tren_pm10(main_df)
    compare_pm10(main_df)

with tab3:
    st.subheader("Tren Kualitas Udara Berdasarkan SO2 di tiap Station")
    plt.figure(figsize=(20, 10))
    sns.lineplot(x='year', y='SO2', hue='station', data=pollutan_gases_df(main_df), marker='o')

    plt.title('Rata-rata SO2 (Dioksida Belerang) per Stasiun dan Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata SO2')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(plt.gcf())

with tab4:
    st.subheader("Tren Kualitas Udara Berdasarkan NO2 di tiap Station")
    plt.figure(figsize=(20, 10))
    sns.lineplot(x='year', y='NO2', hue='station', data=pollutan_gases_df(main_df), marker='o')

    plt.title('Rata-rata NO2 (Dioksida Nitrogen) per Stasiun dan Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata NO2')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(plt.gcf())

with tab5:
    st.subheader("Tren Kualitas Udara Berdasarkan CO di tiap Station")
    plt.figure(figsize=(20, 10))
    sns.lineplot(x='year', y='CO', hue='station', data=pollutan_gases_df(main_df), marker='o')

    plt.title('Rata-rata CO (Karbon Monoksida) per Stasiun dan Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata CO')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(plt.gcf())

with tab6:
    st.subheader("Tren Kualitas Udara Berdasarkan O3 di tiap Station")
    plt.figure(figsize=(20, 10))
    sns.lineplot(x='year', y='O3', hue='station', data=pollutan_gases_df(main_df), marker='o')

    plt.title('Rata-rata O3 (Ozon) per Stasiun dan Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata O3')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(plt.gcf())

#question 2
st.divider()
st.subheader("Hubungan Besarnya Ozon dengan Kualitas Udara")
corr_ozon(main_df)
st.markdown("terlihat pada heatmap diatas bahwa korelasi O3 dengan polutan lainnya adalah korelasi negatif, dengan kata lain, ketika polutan O3 besar maka polutan lainnya kecil, dan sebaliknya")

#question 3
st.divider()
st.subheader("Hubungan Pengaruh Cuaca Terhadap Kualitas Udara")
corr_all_weather(main_df)
st.markdown("pada heatmap diatas, menunjukan bahwa nilai korelasi `TEMP, PRES, DEWP, dan RAIN` tidak begitu kuat dengan polutan seperti `PM2.5, PM10, SO2, NO2, dan O3`, namun terlihat temperature (`TEMP`) lumayan mempengaruhi `O3`")

#question 4
st.divider()
st.subheader('Tren arah mata angin')
mata_angin(main_df)