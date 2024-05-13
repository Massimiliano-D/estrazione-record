import pymongo
import pandas as pd
from datetime import datetime

# Connessione MongoDB in locale
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["test_db"]
collection = db["test_coll"]

import datetime

def estrazione_record(data):
    
    try:

        # Parsing della data inserita dall'utente
        data_da_filtrare = datetime.datetime.strptime(data, "%Y-%m-%d")

    except ValueError:

        # Se il formato della data non è valido, stampa un messaggio di errore
        print("Formato data non valido. Inserisci la data nel formato YYYY-MM-DD.")
        return
    
    # Query per estrarre i record filtrati per data ($gte = seleziona i documenti in cui il valore del campo specificato
    # è maggiore o uguale a un valore specificato; $lt = seleziona i documenti in cui un determinato campo è inferiore 
    # a un certo valore specificato)
    record = collection.find({"Data": {"$gte": data_da_filtrare, "$lt": data_da_filtrare + datetime.timedelta(days=1)}})

    # Converti record in una lista per assicurarti che sia completamente iterabile
    record_list = list(record)

    if record_list:

        # Estrai solo i valori dei record (senza i "_id" di MongoDB)
        data_dict_list = [record_dict for record_dict in record_list]

        # Creazione del DataFrame
        df = pd.DataFrame(data_dict_list)
        
        # Salvataggio del DataFrame in un file Excel
        nome_file = f"estrazione_record_{data}.xlsx"
        df.to_excel(nome_file, index=False)

        print(f"File Excel '{nome_file}' salvato con successo.")

    else:

        # Se nessun record è stato trovato per la data specificata, stampa un messaggio
        print("Nessun record trovato per la data specificata.")

# Questa condizione verifica se il modulo è eseguito come script principale.
if __name__ == "__main__":
    data_da_filtrare = input("Inserisci la data nel formato YYYY-MM-DD: ")
    estrazione_record(data_da_filtrare)