import psycopg2
from gensim.models import Word2Vec

# Load the Word2Vec model
word2vec_model = Word2Vec.load('embeddings/word2vec_model.bin')

# Serialize the Word2Vec model to binary data
serialized_model = word2vec_model.wv.vectors.tobytes()

# Connect to PostgreSQL (replace with your database connection parameters)
conn = psycopg2.connect(
    dbname='wordembedding',
    user='postgres',
    password='root',
    host='localhost',
    port='5432'
)

# Create a table to store the Word2Vec model
with conn.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS word2vec_model (
            id SERIAL PRIMARY KEY,
            model_data BYTEA
        )
    ''')

# Insert the serialized model into the PostgreSQL database
with conn.cursor() as cursor:
    cursor.execute('INSERT INTO word2vec_model (model_data) VALUES (%s)', (serialized_model,))

# Commit the changes and close the connection
conn.commit()
conn.close()
