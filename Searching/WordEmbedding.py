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
        print('Started loading GLOVE')
        self.initValues()
        self.tree = spatial.KDTree(self.glove_embed)
        print('Loaded GLOVE')




    def initValues(self):


        filename = '../glove.6B/glove.6B.50d.txt'

        file = open(filename, 'r', encoding='UTF-8')
        fileLines = file.readlines()
        file.close()
        for line in fileLines:
            row = line.strip().split(' ')
            vocab_word = row[0]
            self.glove_vocab.append(vocab_word)
            embed_vector = [float(i) for i in row[1:]]  # convert to list of float
            self.embedding_dict[vocab_word] = embed_vector
            self.glove_embed.append(embed_vector)


    def __getWordsFromVector(self, vector: np.ndarray):
        nearest_words = [self.glove_vocab[i] for i in vector]
        return nearest_words


    def __getNearest_inxFromVector(self, vector, N=5):
        nearest_dist, nearest_idx = self.tree.query(vector, N)
        return nearest_dist, nearest_idx


    def __getTopNSimilarWords(self, word: str, N: int=5)-> list:
        nearest_dist, nearest_idx = self.__getNearest_inxFromVector(self.embedding_dict[word.lower()], N)
        nearest_words = self.__getWordsFromVector(nearest_idx)
        return nearest_words


    def expandQuery(self, queryList:list)-> list:
        expandedQuery = set()
        for word in queryList:
            expandedQuery = expandedQuery.union(self.__getTopNSimilarWords(word=word))

        if len(queryList) > 1:
            expandedQuery = expandedQuery.union(self.__getTopNSimilarWordsFromWordsList_avgVector(queryList))
        return list(expandedQuery)


    def __getTopNSimilarWordsFromWordsList_avgVector(self, words:list, N: int=5) -> list:
        start = datetime.now()
        finalVector = np.array(self.embedding_dict[words[0]])
        for index in range(1,len(words)):
            finalVector += np.array(self.embedding_dict[words[index].lower()])
        finalVector /= len(words)
        nearest_dist, nearest_idx = self.__getNearest_inxFromVector(finalVector, N)
        nearest_words = self.__getWordsFromVector(nearest_idx)
        finish = datetime.now()
        print("Took: ", str((start - finish).microseconds))
        return nearest_words



