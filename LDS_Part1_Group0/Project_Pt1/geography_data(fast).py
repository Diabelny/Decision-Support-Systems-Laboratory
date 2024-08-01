import csv


from scipy.spatial import cKDTree

def create_city_state_dict():
    #Lettura file delle città + ricerca degli indici degli attributi di interesse
    dataset1 = {}
    with open('uscities.csv', 'r') as file1:
       reader = csv.reader(file1)
       header = next(reader, None)
       lat_index = header.index("lat") 
       lng_index = header.index("lng")
       city_index = header.index("city")
       state_index = header.index("state_name")
       for row in reader:
            # estrazione valori latitudine,longitudine,città,stato
            lat, lon, city, state = float(row[lat_index]), float(row[lng_index]), row[city_index], row[state_index]

            dataset1[(lat, lon)] = (city, state)
            
    sorted_coordinates = dict(sorted(dataset1.items(), key=lambda x: (x[0][0],x[0][1]))  )  
    return sorted_coordinates # dizionario con key=(lat,long) value=(city,state)        

dataset1 = create_city_state_dict()

def create_lat_long_set():
    #Lettura file Police + ricerca degli indici degli attributi di interesse
    dataset2 = set()  
    with open('Police_crime.csv', 'r') as file2:
        reader = csv.reader(file2)
        header = next(reader)
        lat_index = header.index("latitude") 
        lng_index = header.index("longitude")
        for row in reader:
            lat, lon = float(row[lat_index]), float(row[lng_index])# estrazione valori latitudine,longitudine
            dataset2.add((lat, lon))
    sorted_dataset = (sorted(dataset2, key=lambda x: (x[0],x[1])))
          
    return sorted_dataset # insieme tuple univoche (latitude,longitude)  


dataset2 = create_lat_long_set()

    

def map_city_state(dataset1,dataset2):                         
    # Tolleranza per la comparazione delle coordinate
    tol = 0.0001
    dataset2_list = list(dataset2)
    #cKDTree con le coordinate del dataset1
    tree = cKDTree(list(dataset1.keys()))
    
   
    
    # Creare il nuovo dizionario con le corrispondenze
    mapping= {}
    while len(mapping) < len(dataset2):
        dataset2_copy = dataset2_list.copy()

        # Trovare i vicini più prossimi nel dataset1 per ogni coordinata nel dataset2
        distances, indices = tree.query(dataset2_list, k=1, distance_upper_bound=tol)
        
        for i, index in enumerate(indices):
            if index < len(dataset1) and distances[i] <= tol:
                coord2 = dataset2_copy[i]  # Usare la copia anziché l'originale
                coord1 = list(dataset1.keys())[index]
                mapping[coord2] = dataset1.get(coord1)
                dataset2_list.remove(coord2)  # Rimuovere dalla lista originale
                print(coord2, dataset1.get(coord1),len(mapping),tol)
        
        # Aumentare la tolleranza gradualmente
        tol += 0.0001

            
    return mapping                     
                    

mapping = map_city_state(dataset1, dataset2)

with open('../data_results/Geography.csv', 'w', newline='') as geography_file:
        writer = csv.writer(geography_file)
        writer.writerow(['geography_id', 'latitude', 'longitude', 'city', 'state'])  

        geography_id = 0# ID per gli indici  

        for coord, (city, state) in mapping.items():
            writer.writerow([geography_id, coord[0], coord[1], city, state])
            geography_id += 1 
