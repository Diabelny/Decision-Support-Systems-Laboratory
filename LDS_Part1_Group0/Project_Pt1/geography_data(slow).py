import csv
from geopy.distance import great_circle


uscities_data = []
with open('uscities.csv', 'r') as uscities_file:
    uscities_reader = csv.DictReader(uscities_file)
    for row in uscities_reader:
        lat = float(row['lat'])
        lon = float(row['lng'])
        city = row['city']
        state = row['state_name']
        uscities_data.append((lat, lon, city, state))



# In questo script si cerca il mapping (latitude,longitude) di ogni fatto con la città e stato corretti all'interno del file uscities.csv. 
# In particolare viene utilizzata la funzione great_circle della libreria geopy per trovare la distanza minima tra due punti(rappresentati da coppie di coordinate) terrestri. Basandosi su tale distanza vengono estratte le informazioni sulla città e stato.
with open('../data_results/Geography.csv', 'w', newline='') as output_file:
    fieldnames = ['geography_id', 'latitude', 'longitude', 'city', 'state']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()

    with open('Project_Pt1\Police.csv', 'r') as input_file:
        csv_reader = csv.DictReader(input_file)
        geography_id = 0  

        for row in csv_reader:
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])

            min_distance = float('inf')
            closest_city = "Unknown"
            closest_state = "Unknown"

            for lat, lon, city, state in uscities_data:
                coords1 = (latitude, longitude)
                coords2 = (lat, lon)
                distance = great_circle(coords1, coords2).kilometers
                if distance < min_distance:
                    min_distance = distance
                    closest_city = city
                    closest_state = state

            
            writer.writerow({
                'geography_id': geography_id,
                'latitude': latitude,
                'longitude': longitude,
                'city': closest_city,
                'state': closest_state
            })

            print(f"Record {geography_id} processed.")  
            geography_id += 1  
            
