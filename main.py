import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from concurrent.futures import ThreadPoolExecutor, as_completed

start_time = time.time()  # Marca o tempo de início

geolocator = Nominatim(user_agent="maps-cods-adress-eua", timeout=15)


def get_coordinates(address):
    try:
        location = geolocator.geocode(address)
        if location is not None:
            return (location.longitude, location.latitude)
        else:
            return (None, None)
    except GeocoderTimedOut:
        return (None, None)


def get_coordinates_batch(addresses):
    results = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_address = {executor.submit(get_coordinates, address): address for address in addresses}
        for future in as_completed(future_to_address):
            address = future_to_address[future]
            try:
                result = future.result()
                results[address] = result
            except Exception as exc:
                results[address] = (None, None)
                print(f'Erro ao geocodificar {address}: {exc}')
    return results


df = pd.read_csv("data/address.csv")
df = df.dropna()
df_coordinates = pd.DataFrame(columns=['longitude', 'latitude'])
addresses = df['pickups_address'].tolist()

# Dividindo os endereços em blocos de 10
block_size = 10
num_blocks = len(addresses) // block_size
for i in range(num_blocks):
    start_index = i * block_size
    end_index = (i + 1) * block_size
    block_addresses = addresses[start_index:end_index]
    coordinates = get_coordinates_batch(block_addresses)

    for address, coordinate in coordinates.items():
        print(f"{address}: {coordinate[0]}, {coordinate[1]}")
        df_coordinates = pd.concat([df_coordinates, pd.DataFrame({'longitude': [coordinate[0]], 'latitude': [coordinate[1]]})], ignore_index=True)

# Salva o DataFrame como um arquivo CSV
df_coordinates.to_csv('data/coordinates.csv', index=False)

end_time = time.time()  # Marca o tempo de término

print(f"Tempo de execução: {end_time - start_time} segundos")