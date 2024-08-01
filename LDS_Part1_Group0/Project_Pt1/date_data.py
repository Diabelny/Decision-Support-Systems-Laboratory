import xml.etree.ElementTree as ET
import datetime
import csv 

def get_data_from_XML(file):
    data = []# Lista contenente informazioni di file
    tree = ET.parse(file)
    root = tree.getroot()# elemento radice 
    for item in root:#Iterazione su ciascuna riga del file
         data.append([])# Creazione righe su cui salvare i dati 
         index = len(data) - 1 # indice ultima riga appena aggiunta
         for element in item: 
             data[index].append(element.text)# Inserimento del contenuto all' indice corrente
    return data  # lista di liste. ogni sottolista rappresenta una riga del file e gli elementi della sottolista i valori nelle colonne di quella riga  



# Primitive per estrarre informazioni riguardo gli attributi della tabella Date

def get_year(rows):
   years = [] 
   for item in rows:
     years.append (int(item[0].split('-')[0]))
   return years  
     
def get_month(rows):
 months = []   
 for item in rows:
    months.append ((item[0].split('-')[1]))
 return months   

def get_day(rows):
 days = []   
 for item in rows:
     days.append( int(item[0].split('-')[2].split(' ')[0]))
 return days    

def get_index(rows):
  indexes = []
  for item in rows:
     indexes.append(item[1])
  return indexes   

def get_quarter(months):
    quarters = []
    for month in months:
        if month == '01' or month == '02' or month == '03':
            quarters.append('Q1')
        elif month == '04' or month == '05' or month == '06':
            quarters.append('Q2')
        elif month == '07' or month == '08' or month == '09':
            quarters.append ('Q3')
        else :
            quarters.append('Q4')
    return quarters        

def get_date(rows):
  date = []  
  for item in rows : 
     date.append(item[0].split(' ')[0])
  return date   
     
def get_day_of_the_week(year,month,day):
    days_of_the_week = []
    for y ,m , d in zip(year,month,day):
        date = datetime.date(y, int(m), d)  
        day_of_the_week = date.weekday() # Funzione che restituisce il giorno della settimana 
        days_of_the_week.append(day_of_the_week)
    return days_of_the_week


file = "dates.xml"
rows_xml = get_data_from_XML(file)

date_id = get_index(rows_xml)
date = get_date(rows_xml)
day = get_day(rows_xml)
year = get_year(rows_xml)
month = get_month(rows_xml)
quarter = get_quarter(month)
day_of_the_week = get_day_of_the_week(year, month, day)


with open('../data_results/Dates.csv', "w", newline="") as outputfile:
    writer = csv.writer(outputfile)    
    writer.writerow(["Date_id", "date", "day", "month", "year", "quarter","day_of_the_week"])
    for item in zip(date_id, date, day, month, year, quarter,day_of_the_week):
        writer.writerow(item)









 





    
