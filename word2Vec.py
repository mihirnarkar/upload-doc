from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import os

# Load the combined text file
txt_file_path = os.path.join('uploads', 'combined_text.txt')
with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
    combined_text = txt_file.read()

# Tokenize the text into words
tokenized_text = word_tokenize(combined_text.lower())  # Use lower() to ensure consistency

# Train Word2Vec model
word2vec_model = Word2Vec([tokenized_text], vector_size=100, window=5, min_count=1, workers=4)

# Create the 'embeddings' directory if it doesn't exist
embeddings_dir = 'embeddings'
os.makedirs(embeddings_dir, exist_ok=True)

# Save the Word2Vec model
word2vec_model.save(os.path.join(embeddings_dir, 'word2vec_model.bin'))
