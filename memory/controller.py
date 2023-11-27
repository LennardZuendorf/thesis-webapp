# minimal memory module for saving and loading converstations

# package imports
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

#temporary json db setup
db = TinyDB('db.json',storage=MemoryStorage)
query = Query()

def conversation_mapper(data):
    mapping = {
        {
            'user': 'Hello, how are you?',
            'bot': 'I am good, thank you.'
        },
    }
    return mapping

# function to dump json data into the db
def dump (data):
    mapping = conversation_mapper(data)
    doc_id = db.insert(data)
    return doc_id, mapping

# function to query data from the db
def get (doc_id:int):
    data = db.get(doc_id=doc_id)
    return data
