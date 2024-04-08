import pandas as pd
import folium

def create_map():
    # Lê o DataFrame do arquivo CSV
    df_coordinates = pd.read_csv('data/coordinates.csv')

    # Remove as linhas com valores NaN
    df_coordinates = df_coordinates.dropna(subset=['latitude', 'longitude'])

    map = folium.Map(location=[df_coordinates['latitude'].mean(),df_coordinates['longitude'].mean()],zoom_start=5)

    for idx, row in df_coordinates.iterrows():
        folium.Marker([row['latitude'],row['longitude']]).add_to(map)

    map.save('map.html')

# Chama a função para criar o mapa
create_map()