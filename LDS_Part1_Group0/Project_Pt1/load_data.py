import csv
import pyodbc
import tqdm as tq
import time

# Apertura connessione database 'Group_ID_0_DB' e creazione cursore
server = 'tcp:lds.di.unipi.it'
database = 'Group_ID_0_DB'
username = 'Group_ID_0'
password = '4YOXT7UA'
connectionString = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()

cursor.fast_executemany = True  # abilitazione metodo executemany

print('Start loading ...\n')


# Lettura delle tabelle locali Date,Gun,Partecipant,Geography,Custody presenti nella cartella data_results 

dates=open('../data_results/Dates.csv','r')
dates_rows=csv.reader(dates,delimiter=',')

guns=open('../data_results/Guns.csv','r')
guns_rows=csv.reader(guns,delimiter=',')

partecipants=open('../data_results/Partecipants.csv','r')
partecipants_rows=csv.reader(partecipants,delimiter=',')

geography=open('../data_results/Geography.csv','r')
geography_rows=csv.reader(geography,delimiter=',')

custodies=open('../data_results/Custodies.csv','r')
custodies_rows=csv.reader(custodies,delimiter=',')


# Apertura del file errors per la registrazione dei possibili errori egenrati in fase di caricamento
with open("../data_results/errors.txt", "a") as error_file:

    try:
        
        tables = {
            'Dates': dates_rows,
            'Guns': guns_rows,
            'Partecipants': partecipants_rows,
            'Geography': geography_rows,
            'Custodies': custodies_rows
        }

        

        for table, rows in tables.items(): # Iterazione su tabelle e righe

            
            print(table)
            sql = ''
            data_list=[] # Lista contenente i dati, formattati come tuple, per la i-esima tabella.
            t=time.time() # Registrazione tempo attuale per misurare quanto tempo impiega il caricamento di ogni tabella
            is_header = True

            for row in tq.tqdm(rows, desc=table):
                 # itero su ogni riga della tabella i-esima utilizzando la funzione tqdm per generare una barra di avanzamento del processo.

                if not row: # Caso riga vuota
                    continue

                if is_header: # Caso header
                    attr_counter = 0 # numero colonne i-esima tabella
                    parametric_values = '' # stringa segnaposto ?
                    data_string='' # stringa nomi colonne
                    
                    for el in row: # estrazione informazioni per ogni riga
                        data_string += el + ',' 
                        parametric_values += '?,' 
                        attr_counter +=1

                    sql = f'INSERT INTO {username}.{table}({data_string[:-1]}) VALUES({parametric_values[:-1]})' #  indice -1 per rimuovere la virgola finale della stringa
                    is_header=False 

                else: 
                    if table == 'Dates':
                        date = (int(row[0]),row[1],int(row[2]),int(row[3]),int(row[4]),row[5],int(row[6]))

                    elif table == 'Guns':
                        date = (int(row[0]),row[1],row[2])

                    elif table == 'Partecipants':
                        date = (int(row[0]),row[1],row[2],row[3],row[4])

                    elif table == 'Geography':
                        date = (int(row[0]),float(row[1]),float(row[2]),row[3],row[4])

                    elif table == 'Custodies':
                        date = (int(row[0]),int(row[1]),int(row[2]),int(row[3]),int(row[4]), int(row[5]), int(row[6]))

                    else:
                        raise NameError(f'Unknown Table: {table}')
                    
                    data_list.append(date)

            cursor.executemany(sql,data_list)
            cnxn.commit()
            print(f"Loaded - Table{table} in {time.time() - t} [s]")
            print("********************************************")
            is_header = True
            

    except Exception as e:

        # gestione potenziali eccezioni scaturite a tempo di esecuzione
        error_message = f"Error: {str(e)}\n"
        print(error_message)
        error_file.write(error_message)

    finally:

        # Chiusura descrittori di file 
        dates.close()
        guns.close()
        partecipants.close()
        geography.close()
        custodies.close()

        # Chiusura cursore
        cursor.close()

        # Chiusura connessione 
        cnxn.close()
    
print('End loading\n')