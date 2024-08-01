import csv
import pyodbc
import tqdm as tq


# Apertura connessione database 'Group_ID_0_DB' e creazione cursore
server = 'tcp:lds.di.unipi.it'
database = 'Group_ID_0_DB'
username = 'Group_ID_0'
password = '4YOXT7UA'
connectionString = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()

print('Start truncating ...\n')

cursor.execute('''
                
                truncate table Dates;
                truncate table Guns;
                truncate table Partecipants;
                truncate table Geography;
                truncate table Custodies;

               ''')

cnxn.commit()

# Chiusura cursore
cursor.close()

# Chiusura connessione 
cnxn.close()

print('End\n')