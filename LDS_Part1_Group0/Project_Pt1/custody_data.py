import csv

# Funzione per leggere un file CSV che restituisce un dizionario con key=tupla di valori univoci
def read_csv(filename, id_column, value_columns):
    data = {}
    with open(filename, mode="r", newline="") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            values = row[id_column]
            key = tuple(row[col] for col in value_columns)
            data[key] = values
    return data

# Lettura e creazione dizionario per Geography,Partecipants,Guns
geo_data = read_csv("../data_results/Geography.csv", "geography_id", ["latitude", "longitude"])
partecipant_data = read_csv("../data_results/Partecipants.csv", "partecipant_id", ["age_group", "gender", "status", "type"])
gun_data = read_csv("../data_results/Guns.csv", "gun_id", ["is_stolen", "gun_type"])

# Creazione lista di dizionari per ogni riga
custody_data = []
with open("Police_crime.csv", mode="r", newline="") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        custody_data.append({
            "custody_id": row["custody_id"],
            "date_fk": row["date_fk"],
            "incident_id": row["incident_id"],
            "crime_gravity": row["crime_gravity"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "gun_stolen": row["gun_stolen"],
            "gun_type": row["gun_type"],
            "participant_age_group": row["participant_age_group"],
            "participant_gender": row["participant_gender"],
            "participant_status": row["participant_status"],
            "participant_type": row["participant_type"]
        })

# Estrazione FK per ogni fatto nella lista di dizionari rappresentante il file Police_crime.csv
geo_id = [geo_data[custody["latitude"], custody["longitude"]] for custody in custody_data]
partecipant_id = [partecipant_data[custody["participant_age_group"], custody["participant_gender"], custody["participant_status"], custody["participant_type"]] for custody in custody_data]
gun_id = [gun_data[custody["gun_stolen"], custody["gun_type"]] for custody in custody_data]

# Creazione tabella Custodies con le informazioni appropriate
with open("../data_results/Custodies.csv", mode="w", newline="") as output_file:
    fieldnames = ["custody_id","partecipant_id","gun_id","geo_id","date_id", "incident_id", "crime_gravity"]
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(fieldnames)
    for custody, geo, partecipant, gun in zip(custody_data, geo_id, partecipant_id, gun_id):
        csv_writer.writerow([
            custody["custody_id"],
            partecipant,
            gun,
            geo,
            custody["date_fk"],
            custody["incident_id"],
            custody["crime_gravity"],
            ])
