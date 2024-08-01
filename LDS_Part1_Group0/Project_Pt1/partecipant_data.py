import csv

file_input = 'Police_crime.csv'
file_output = '../data_results/Partecipants.csv'

with open(file_output, 'w', newline='') as output_file:

    
    fieldnames = ['partecipant_id', 'age_group', 'gender', 'status','type']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader() 

    with open(file_input, 'r') as input_file:
        csv_reader = csv.DictReader(input_file)

        #Insieme per salvare le coppie univoche
        unique_keys = set()

        participant_id_counter = 0#Contatore per gli ID   

        for row in csv_reader:
            age_group = row['participant_age_group']
            gender = row['participant_gender']
            status = row['participant_status']
            partecipant_type = row['participant_type']

            key = (age_group, gender, status, partecipant_type)

            #Controllo se la tupla univoca è già presente
            if key not in unique_keys:
                writer.writerow({
                    'partecipant_id': participant_id_counter,
                    'age_group': age_group,
                    'gender': gender,
                    'status': status,
                    'type':partecipant_type
                })
                unique_keys.add(key)
                participant_id_counter += 1  
