
import os
import re
import gensim

from Parsing.IterativeParsing import IterativeTokenizer
from BasicMethods import getTagFromText
from datetime import datetime



class MyEmbedderTokenizer(IterativeTokenizer):

    def __init__(self, stopwordPath):
        try:
            super().__init__(None)
        except AttributeError as err:
            pass
        stopWordPath = stopwordPath
        self.stopWordsDic = {}

        try:
            import os
            path = stopWordPath
            with open(path) as f:
                for word in f.read().splitlines():
                    self.stopWordsDic[word] = 'a'
                del self.stopWordsDic["may"]
        except IOError:
            print("Can't find path:", stopwordPath)

    def parseText(self,text):

        self.betweenPattern.sub(self.replaceBetween, text)
        import lxml.html
        t = lxml.html.fromstring(text)
        text = t.text_content()

        text = text.replace("\n", ' ').replace('\t', ' ').replace("'s", '').replace('{', ' ').replace('}', ' ').replace('[', ' ').replace(']',
                                                                                                                   ' ').replace(
            '\"', ' ').replace('\'', ' ').replace('(', ' ').replace(')', ' ').replace('?', ' ').replace('!', ' ').replace('#',
                                                                                                                    ' ').replace(
            '@', ' ').replace('/', ' ').replace('\\', ' ').replace('_', ' ').replace('>', ' ').replace('<', ' ').replace('`',
                                                                                                                   ' ').replace(
            '~', ' ').replace(';', ' ').replace(':', ' ').replace('*', ' ').replace('+', ' ').replace('|', ' ').replace('&',
                                                                                                                  ' ').replace(
            '=', ' ')
        text = re.sub(r'[-]+','-',text)
        text = re.sub(r'[.]+', '.', text)
        text = re.sub(r'[,]+', ',', text)
        text = re.sub(r'[ ]+', ' ', text)
        splittedText = text.split(' ')
        return self.parseList(splittedText)


    def parseList(self, termList):
        from Stemmer import Stemmer
        termList = list(filter(self.filterAll, termList))

        finalTermList = []

        for term in termList:
            if any(char.isdigit() for char in term):
                continue
            term = term.lower()
            if '-' in term:
                finalTermList += self.parseList(term.split('-'))
            elif term.count(',') > 0 :
                finalTermList += self.parseList(term.split(','))
            elif term.count('.') > 0:
                finalTermList += self.parseList(term.split('.'))

            cleanedWord = term.strip(',').strip('.')

            if self.dictionary_term_stemmedTerm.get(cleanedWord) is None:
                afterStem = Stemmer.stemTerm(cleanedWord)
                self.dictionary_term_stemmedTerm[cleanedWord] = afterStem
            else:
                afterStem = self.dictionary_term_stemmedTerm[cleanedWord]

            finalTermList.append(afterStem)

        return finalTermList





class MySentences(object):
    def __init__(self, dirname, stopwordPath):
        self.dirname = dirname
        self.iterationNumber = 0
        try:
            self.tokenizer = MyEmbedderTokenizer(stopwordPath)
        except AttributeError as err:
            pass

    def __iter__(self):
        counter = 0
        self.iterationNumber += 1

        filesList = os.listdir(self.dirname)
        for fname in filesList:
            with open(os.path.join(self.dirname, fname)) as file:
                counter += 1
                if counter % 50000 == 0:
                    print ('IterNum: ' + str(self.iterationNumber),datetime.now(), str(counter) + '/' + str(len(filesList)) + " files processed")

                text = file.read()
                onlyText = getTagFromText(text, "<TEXT>", "</TEXT>")
                findTextSquared = onlyText.find('[Text]')
                if findTextSquared > 0:
                    onlyText = onlyText[findTextSquared + len('[Text]'):]

                if len(onlyText) < 10:
                    continue

                parsedText = self.tokenizer.parseText(onlyText)
                yield parsedText






class EmbeddingCreator(object):

    def __init__(self, corpusPath:str='', outputPath:str='', stopwordsPath:str=''):
        self._corpusPath = corpusPath
        self._outputPath = outputPath
        self._stopwordsPath = stopwordsPath

    def setCorpusPath(self, path):
        self._corpusPath = path

    def setOutputPath(self, path):
        self._outputPath = path

    def setStopwordsPath(self, path):
        self._stopwordsPath = path

    def createModel(self):
        from gensim.models import word2vec
        print('Stared creating the model')

        start = datetime.now()
        sentences = MySentences(self._corpusPath, self._stopwordsPath)  # a memory-friendly iterator
        model = None
        if word2vec.FAST_VERSION == 1:
            model = gensim.models.Word2Vec(sentences, min_count=1, workers=4)
        else:
            model = gensim.models.Word2Vec(sentences, min_count=1)

        if model is not None:
            model.save(self._outputPath)
            print ('model was built successfully')
        finish = datetime.now()
        took = start - finish
        print("Took: ", str(took.seconds/60) + 'Minutes')

        return model


    def createModelFromGlove(self, pathOfGlove, dimensions):
        # https://datascience.stackexchange.com/questions/10695/how-to-initialize-a-new-word2vec-model-with-pre-trained-model-weights
        from gensim.models import word2vec
        from gensim.models import KeyedVectors
        print('Stared creating the model')

        start = datetime.now()
        sentences = MySentences(self._corpusPath, self._stopwordsPath)  # a memory-friendly iterator
        model = None
        if word2vec.FAST_VERSION == 1:
            model = gensim.models.Word2Vec(size=dimensions, min_count=4, workers=4)

        else:
            model = gensim.models.Word2Vec(size=dimensions, min_count=4)

        model.build_vocab(sentences)
        total_examples = model.corpus_count



         # call glove2word2vec script
         # default way (through CLI): python -m gensim.scripts.glove2word2vec --input <glove_file> --output <w2v_file>
        from gensim.scripts.glove2word2vec import glove2word2vec
        # glove2word2vec(pathOfGlove, "C:/SavedModel/glove2Word2vec_stemmedAndStopWord")

        # model = KeyedVectors.load_word2vec_format(tmp_file)

        # modelGlove = KeyedVectors.load_word2vec_format("C:/SavedModel/glove2Word2vec_stemmedAndStopWord", binary=False)
        modelGlove = KeyedVectors.load_word2vec_format("C:/SavedModel/glove2Word2vec", binary=False)

        model.build_vocab([list(modelGlove.vocab.keys())], update=True)
        model.intersect_word2vec_format("C:/SavedModel/glove2Word2vec", binary=False, lockf=1.0)
        model.train(sentences, total_examples=total_examples, epochs=model.iter)
        if model is not None:
            model.save(self._outputPath)
            print ('model was built successfully')
        finish = datetime.now()
        took = finish - start
        print("Took: ", str(took.seconds/60) + ' Minutes')


        return model


class WordEmbeddingUser(EmbeddingCreator):

    def __init__(self, modelPath:str, corpusPath =''):
        super(WordEmbeddingUser, self).__init__(corpusPath=corpusPath,outputPath=modelPath)
        self._modelPath = modelPath
        self._model = None
        self.wv = None

    def setModelPath(self, path):
        self._modelPath = path

    def createModel(self):
        if (super(WordEmbeddingUser, self)._stopwordsPath != '' and os.path.exists(super(WordEmbeddingUser, self)._stopwordsPath)) and (super(WordEmbeddingUser, self)._outputPath != '' and os.path.exists(super(WordEmbeddingUser, self)._outputPath)) and super(WordEmbeddingUser, self)._corpusPath != '' and os.path.exists(super(WordEmbeddingUser, self)._corpusPath):
            self._model = super().createModel()
        else:
            return False
        return self._model is None

    def loadModel(self):
        try:
            self._model = gensim.models.Word2Vec.load(self._modelPath)
            self.wv = self._model.wv
            return True
        except Exception as err:
            print (err)
            return False

    def getModel(self):
        return self._model

    def getTopNSimilarWords(self, word ,N=5):
        try:
            # mostSimilar = self._model.wv.similar_by_word(word=word, topn=N)
            mostSimilar = self._model.most_similar(word, topn=N)
            # tempVector = self._model.wv.word_vec(word=word, use_norm=True)
            # tempVector = self._model.wv[word]
            # mostSimilar = self._model.wv.similar_by_vector(tempVector, topn=N)
            finalResults = []
            print ('Word: ', word)
            for word_sim in mostSimilar:
                print ('\t',word_sim)
                if word_sim[0] == word or word_sim[1] >= 1:
                    continue
                finalResults.append(word_sim)
            print("\n\n*******************   TOP SIMILAR  *************")
            print("Results = ",finalResults,"\n")
            return finalResults
        except Exception as err:
            # print (err)
            return None

    def getTopNSimilarWordsFromList(self, wordList ,N=5):
        finalVector = None
        for word in wordList:
            try:
                tempVector = self._model.wv.word_vec(word=word, use_norm=True)
                if finalVector is None:

                    finalVector = tempVector
                else:
                    finalVector += tempVector
            except :
                pass
        if finalVector is not None:
            mostSimilar = self._model.wv.similar_by_vector(finalVector, topn=10)
            finalResults = []
            for word_sim in mostSimilar:
                if word_sim[0] in wordList or word_sim[1] >= 1:
                    continue
                finalResults.append(word_sim)
            return finalResults

        return None





    # def getTopNSimilarWordsFromList(self, wordList: list ,N:int=5)->list or None:
    #     try:
    #         mostSimilar = self._model.most_similar(positive=wordList, topn=N)
    #         return mostSimilar
    #     except Exception as err:
    #         print (err)
    #         return None

    # def expandQuery(self,queryList:list)->list:
    #     if self._model is None:
    #         return queryList
    #     expandedQuery = set()
    #     for word in queryList:
    #         if self._model[word.lower()] is not None:
    #             mostSimilar = self.getTopNSimilarWords(word=word.lower())
    #             if mostSimilar is not None:
    #                 expandedQuery = expandedQuery.union(mostSimilar)
    #
    #     if len(queryList) > 1:
    #         lowerList = []
    #         for w in queryList:
    #             lowerList.append(w.lower())
    #         mostSimilar = self.getTopNSimilarWordsFromList(wordList=lowerList)
    #         if mostSimilar is not None:
    #             expandedQuery = expandedQuery.union(mostSimilar)
    #     return list(expandedQuery)

    def visualizeMyModel(self):
        if self._model is not None:
            self.visualizeModel(self._model)


    @staticmethod
    def visualizeModel(model):
        from sklearn.manifold import TSNE
        import pandas as pd
        import matplotlib.pyplot as plt

        vocab = list(model.wv.vocab)
        X = model[vocab]

        tsne = TSNE(n_components=2)
        X_tsne = tsne.fit_transform(X)

        df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        ax.scatter(df['x'], df['y'])

        # ax.set_xlim()
        # ax.set_ylim()

        for word, pos in df.iterrows():
            ax.annotate(word, pos)
        plt.show()


    @staticmethod
    def otherVisualizationModel(model):
        from sklearn.manifold import TSNE
        import matplotlib.pyplot as plt


        "Creates and TSNE model and plots it"
        labels = []
        tokens = []

        for word in model.wv.vocab:
            tokens.append(model[word])
            labels.append(word)

        tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
        new_values = tsne_model.fit_transform(tokens)

        x = []
        y = []
        for value in new_values:
            x.append(value[0])
            y.append(value[1])

        plt.figure(figsize=(16, 16))
        for i in range(len(x)):
            plt.scatter(x[i], y[i])
            plt.annotate(labels[i],
                         xy=(x[i], y[i]),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')
        plt.show()




corpusPath = "C:/AllDocs"
outputPath = "C:/SavedModel/mymodel.model"
tempPath = "C:/SavedModel/glove2Word2vec_stemmedAndStopWord"
stopWordsPath = "C:/stop_words.txt"
pathOfGlove = "C:/mat100.txt"

# manager = EmbeddingCreator(corpusPath=corpusPath,outputPath=outputPath,stopwordsPath=stopWordsPath)
# manager.createModel()
# from gensim.models import KeyedVectors
# modelGlove = KeyedVectors.load_word2vec_format("C:/SavedModel/glove2Word2vec_stemmedAndStopWord", binary=False)


# creator = EmbeddingCreator(corpusPath=corpusPath,outputPath=outputPath,stopwordsPath=stopWordsPath)
# model = creator.createModelFromGlove(pathOfGlove=tempPath,dimensions=100)
#
#








# creator = EmbeddingCreator(corpusPath=corpusPath,outputPath=outputPath,stopwordsPath=stopWordsPath)
# model = creator.createModelFromGlove(pathOfGlove=pathOfGlove,dimensions=100)
from gensim.scripts.glove2word2vec import glove2word2vec


# from gensim.models import KeyedVectors
# glove2word2vec(tempPath, "C:/SavedModel/glove2Word2vec")
# modelGlove = KeyedVectors.load_word2vec_format("C:/SavedModel/glove2Word2vec", binary=False)
# print ("model loaded")

#
#
# import numpy as np
# from numpy import array
# from Stemmer import Stemmer
# stopWordsDic = {}
#
# try:
#     import os
#
#     path = stopWordsPath
#     with open(path) as f:
#         for word in f.read().splitlines():
#             stopWordsDic[word] = 'a'
#         del stopWordsDic["may"]
# except IOError:
#     print("Can't find path:", stopWordsPath)
#
# def createVector(numbersListOfStrings):
#     vector = []
#     for x in numbersListOfStrings:
#         vector.append(float(x))
#     return vector
#
#
# def createStringListFromVector(numbersListOfStrings):
#     vector = []
#     for x in numbersListOfStrings:
#         stringNum = "%.6f" % x
#         vector.append(stringNum)
#     return vector
#
# file = open(pathOfGlove,'r', encoding='utf-8')
# fileLineList = file.readlines()
# dictionary_term_arr = dict()
# for line in fileLineList:
#     splitLine = line.split(' ')
#     term = splitLine[0]
#     if stopWordsDic.get(term) is None:
#         stemmedTerm = Stemmer.stemTerm(term)
#         if stemmedTerm is not None:
#             if dictionary_term_arr.get(stemmedTerm) is None:
#
#                 vector = createVector(splitLine[1:])
#                 numpyArray = array(vector, dtype=np.float64)
#                 dictionary_term_arr[stemmedTerm] = [vector, 0]
#             else:
#                 numberOfAverage = dictionary_term_arr[stemmedTerm][1]
#                 vector = createVector(splitLine[1:])
#                 numpyArray = array(vector, dtype=np.float64)
#                 newVector = (numpyArray + ((numberOfAverage + 1) * dictionary_term_arr[stemmedTerm][0])) / (numberOfAverage + 2)
#                 dictionary_term_arr[stemmedTerm] = [newVector, numberOfAverage + 1]
#
#
# outputNewGlovePath = "C:/SavedModel/glove2Word2vec_stemmedAndStopWord"
# with open(outputNewGlovePath,'w+', encoding='utf-8') as outputNewGlovePathFile:
#
#     for term, vector_avg in dictionary_term_arr.items():
#         strList = createStringListFromVector(vector_avg[0])
#
#         lineToWrite = ' '.join([term] + strList) + '\n'
#
#         outputNewGlovePathFile.write(lineToWrite)
#
#
#





