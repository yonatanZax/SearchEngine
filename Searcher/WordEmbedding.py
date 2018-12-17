from scipy import spatial
import numpy as np
from datetime import datetime

class WordEmbedding:

    def __init__(self):
        """
        http://www.brightideasinanalytics.com/pretrained-word-vectors-example/
        glove_vocab – list of the words that we now have embeddings for
        glove_embed – list of lists containing the embedding vectors
        embedding_dict – dictionary where the words are the keys and the embeddings are the values
        """
        self.glove_vocab = []
        self.glove_embed = []
        self.embedding_dict = {}
        self.initValues()
        self.tree = spatial.KDTree(self.glove_embed)
        print('Loaded GLOVE')




    def initValues(self):

        print('Started loading GLOVE')

        filename = '../../glove.6B/glove.6B.50d.txt'

        file = open(filename, 'r', encoding='UTF-8')

        for line in file.readlines():
            row = line.strip().split(' ')
            vocab_word = row[0]
            self.glove_vocab.append(vocab_word)
            embed_vector = [float(i) for i in row[1:]]  # convert to list of float
            self.embedding_dict[vocab_word] = embed_vector
            self.glove_embed.append(embed_vector)

        file.close()

    def getWordsFromVector(self, vector: np.ndarray):
        nearest_words = [self.glove_vocab[i] for i in vector]
        return nearest_words

    def getNearest_inxFromVector(self, vector, N):
        nearest_dist, nearest_idx = self.tree.query(vector, N)
        return nearest_dist, nearest_idx


    def getTopNSimilarWords(self, word: str, N: int)-> list:
        nearest_dist, nearest_idx = self.getNearest_inxFromVector(self.embedding_dict[word], N)
        nearest_words = self.getWordsFromVector(nearest_idx)
        return nearest_words


    def getTopNSimilarWordsFromWordsList(self, words:list, N: int) -> list:
        start = datetime.now()
        finalVector = np.array(self.embedding_dict[words[0]])
        for index in range(1,len(words)):
            finalVector += np.array(self.embedding_dict[words[index]])
        finalVector /= len(words)
        nearest_dist, nearest_idx = self.getNearest_inxFromVector(finalVector, N)
        nearest_words = self.getWordsFromVector(nearest_idx)
        finish = datetime.now()
        print("Took: ", str((start - finish).microseconds))
        return nearest_words





def test():
    wordEmbedding = WordEmbedding()

    nearestWord = wordEmbedding.getTopNSimilarWordsFromWordsList(['king','man','woman'], 10)
    print (nearestWord)


test()

