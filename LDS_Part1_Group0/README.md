Repository of Laboratory of Data Science Project Pt 1 
Decision Support Systems - Module II (6 ECTS): LABORATORY OF DATA SCIENCE (2023/2024)


**Flusso di lavoro prima parte progettuale**

Assignment 0 -> Creazione schema database usando SQL Server Management Studio

Assignment 1 -> [ET(L) Process] Creazione tabelle lato client  usando Python

Assignment 2 -> [(ET)L Process] Caricamento dati Su SQL Server usando Python


**Flusso esecuzione script**

 crime_gravity.py -> calcolo misura principale del fatto e generazione file Police_crime.csv, sorgente dei successivi script

 date_data.py -> creazione tabella Dates.csv

 gun_data.py -> creazione tabella Guns.csv

 partecipant_data -> creazione tabella Partecipants.csv

 geography_data(fast).py || geography_data(slow).py -> creazione tabella Geography.csv

 custody_data.py -> creazione tabella Custodies

 load_data.py -> caricamento tabella su SQL Server

 truncate.py -> cancellazione tabelle database su SQL Server


N.B. Tutti i file csv corrispondenti vengono generati nella cartella data_results, contenente anche il errors.txt in cui verranno registrati potenziali errori a tempo di esecuzione derivanti dallo script load_data.py