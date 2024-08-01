import csv
import json


fact_table = [] # Lista contenente record di Police.csv

with open('Police.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        fact_table.append(row)

with open('dict_partecipant_status.json', 'r') as status_file:
    status_dict = json.load(status_file)

with open('dict_partecipant_type.json', 'r') as type_file:
    type_dict = json.load(type_file)

with open('dict_partecipant_age.json', 'r') as age_group_file:
    age_group_dict = json.load(age_group_file)


# Calcolo crime_gravity per ogni record

for record in fact_table:
    status_key = record['participant_status']
    type_key = record['participant_type']
    age_key = record['participant_age_group']
    
    status_value = status_dict.get(status_key) 
    type_value = type_dict.get(type_key)
    age_group_value = age_group_dict.get(age_key)
    
    # Crime gravity per ogni record 
    total_value = age_group_value * type_value  * status_value
    print(f"Record: {record}, Crime Gravity: {total_value}")
    record['crime_gravity']=total_value


# Creazione file Police_crime.csv  con la colonna relativa al crime_gravity
new_column_names = fact_table[0].keys()
with open('Police_crime.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=new_column_names)
    csv_writer.writeheader()
    csv_writer.writerows(fact_table)

print('Colonna "crime_gravity" aggiunta con successo al nuovo file Police')

# Sostituzione valori Unknown con NULL per le colonne gun_type e gun_stolen
with open('Police_crime.csv', 'r') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

for row in rows:
    row['gun_type'] = 'NULL' if row['gun_type'] == 'Unknown' else row['gun_type']
    row['gun_stolen'] = 'NULL' if row['gun_stolen'] == 'Unknown' else row['gun_stolen']

# Aggiornamento Police_crime
fieldnames = reader.fieldnames
with open('Police_crime.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
