import pymongo
import random
from datetime import datetime, timedelta

# Connessione MongoDB in locale
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["test_db"]
collection = db["test_coll"]

# Funzione per la creazione della data randomica nell'intervallo richiesto
def generate_random_date():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2022, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date 

# Verifica se ci sono già 10000 record nel database
existing_records_count = collection.count_documents({})
if existing_records_count < 10000:
    start_id = 1
else:
    # Se ci sono già 10000 record, inizia dall'ID successivo
    max_id_record = collection.find().sort("Id", -1).limit(1)
    max_id_value = max_id_record[0]["Id"]
    start_id = max_id_value + 1

while True:
    # Creo l'URL utilizzando il numero corrente del range
    url = f"https://test.it/demo/{start_id}"
    
    # Ottengo il timestamp corrente per data_inserimento
    data_inserimento = datetime.now()
    
    # Genera una data casuale
    data = generate_random_date()
    
    # Creo il dizionario per il record
    record = {"Url": url, "Id": start_id, "DataInserimento": data_inserimento, "Data": data}
    
    # Controlla se esiste con il valore Url
    record_esistente = collection.find_one({"Url": url})
    
    # Se non viene trovato un record esistente, viene inserito
    if record_esistente is None:
        collection.insert_one(record)
    
    # Incrementa l'ID per l'iterazione successiva
    start_id += 1
    
    # Esci dal ciclo una volta raggiunti i 10000 record
    if existing_records_count >= 10000 and start_id >= max_id_value + 10000:
        break
