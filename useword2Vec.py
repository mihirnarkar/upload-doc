from gensim.models import Word2Vec

# Load the Word2Vec model
word2vec_model = Word2Vec.load('embeddings/word2vec_model.bin')

# Example usage
word_vector = word2vec_model.wv['relu']
print(f"Vector for 'example_word': {word_vector}")
