import json
import uuid
from pymongo import MongoClient, errors

# Conectar a MongoDB
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client.table_llm  # Seleccionar la base de datos
except errors.ConnectionFailure as e:
    print("Error al conectar a MongoDB:", e)
    exit(1)

def insert_chat(question, answer, file_detail):
    """Inserta un nuevo chat en la colección 'chat'."""
    session_id = str(uuid.uuid1())
    try:
        db.chat.insert_one({
            'session_id': session_id,
            'question': question,
            'answer': answer,
            'file_detail': file_detail,
            'vote': 0
        })
        return session_id
    except errors.PyMongoError as e:
        print("Error al insertar chat:", e)
        return None

def update_vote_by_session_id(vote, session_id):
    """Actualiza el voto para un chat dado su session_id."""
    try:
        res = db.chat.update_one(
            {'session_id': session_id},
            {'$set': {'vote': vote}}
        )
        return res.modified_count  # Retorna el número de documentos modificados
    except errors.PyMongoError as e:
        print("Error al actualizar voto:", e)
        return None

def get_random_wtq():
    """Obtiene un documento aleatorio de la colección 'wtq'."""
    try:
        res = list(db.wtq.aggregate([{ '$sample': { 'size': 1 } }]))
        return res[0] if res else None  # Retorna None si no hay resultados
    except errors.PyMongoError as e:
        print("Error al obtener documento aleatorio de wtq:", e)
        return None

def get_random_table_op():
    """Obtiene un documento aleatorio de la colección 'table_op'."""
    try:
        res = list(db.table_op.aggregate([{ '$sample': { 'size': 1 } }]))
        return res[0] if res else None  # Retorna None si no hay resultados
    except errors.PyMongoError as e:
        print("Error al obtener documento aleatorio de table_op:", e)
        return None

def get_random_table_merge():
    """Obtiene un documento aleatorio de la colección 'table_merge'."""
    try:
        res = list(db.table_merge.aggregate([{ '$sample': { 'size': 1 } }]))
        return res[0] if res else None  # Retorna None si no hay resultados
    except errors.PyMongoError as e:
        print("Error al obtener documento aleatorio de table_merge:", e)
        return None