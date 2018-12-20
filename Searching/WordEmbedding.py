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


        filename = '../WordEmbedding/glove.6B.50d.txt'
        # filename = '../glove.6B/glove.6B.50d.txt'

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
        expandedQuery = set(queryList)
        for word in queryList:
            expandedQuery = expandedQuery.union(self.__getTopNSimilarWords(word=word))

        if len(queryList) > 1:
            expandedQuery = expandedQuery.union(self.__getTopNSimilarWordsFromWordsList_avgVector(queryList))
        return list(expandedQuery)


    def __getTopNSimilarWordsFromWordsList_avgVector(self, words:list, N: int=5) -> list:
        start = datetime.now()

        i = 0
        j = 0
        # Skip None words in list
        while  j  < len(words):
            if self.embedding_dict.get(words[j].lower()) is None:
                j += 1
            else:
                i = j
                break

        if i == 0 and j > 0:
            return []
        finalVector = np.array(self.embedding_dict[words[i].lower()])

        for index in range(i + 1,len(words)):
            if self.embedding_dict.get(words[index].lower()) is None:
                continue
            finalVector += np.array(self.embedding_dict[words[index].lower()])
        finalVector /= len(words)
        nearest_dist, nearest_idx = self.__getNearest_inxFromVector(finalVector, N)
        nearest_words = self.__getWordsFromVector(nearest_idx)
        finish = datetime.now()
        print("Took: ", str((start - finish).microseconds))
        return nearest_words






