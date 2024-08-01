import csv        

file_input = 'Police_crime.csv'
file_output = '../data_results/Guns.csv'

with open(file_output, 'w', newline='') as output_file:

    fieldnames = ['gun_id', 'gun_type', 'is_stolen']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader() 

    with open(file_input, 'r') as input_file:
        csv_reader = csv.DictReader(input_file)

        #Insieme per salvare le coppie univoche
        unique_keys = set()

        gun_id_counter = 0#Contatore per gli ID  

        for row in csv_reader:
            gun_type = row['gun_type']
            is_stolen = row['gun_stolen']
            

            key = (gun_type, is_stolen)

            # Controllo se la tupla univoca è già presente
            if key not in unique_keys:
                writer.writerow({
                    'gun_id': gun_id_counter,
                    'gun_type': gun_type,
                    'is_stolen': is_stolen
                    
                })
                unique_keys.add(key)
                gun_id_counter += 1                  
    
            
