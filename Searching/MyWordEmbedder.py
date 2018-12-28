
import os
import re
import gensim

from Parsing.IterativeParsing import IterativeTokenizer
from BasicMethods import getTagFromText
from datetime import datetime



class MyEmbedderTokenizer(IterativeTokenizer):

    def __init__(self, stopwordPath:str):
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

        text = text.replace("\n", ' ').replace('\t', ' ').replace('{', '').replace('}', '').replace('[', '').replace(']',
                                                                                                                   '').replace(
            '\"', '').replace('\'', '').replace('(', '').replace(')', '').replace('?', '').replace('!', '').replace('#',
                                                                                                                    '').replace(
            '@', '').replace('/', '').replace('\\', '').replace('_', '').replace('>', '').replace('<', '').replace('`',
                                                                                                                   '').replace(
            '~', '').replace(';', '').replace(':', '').replace('*', '').replace('+', '').replace('|', '').replace('&',
                                                                                                                  '').replace(
            '=', '')
        text = re.sub(r'[-]+','-',text)
        text = re.sub(r'[.]+', '.', text)
        text = re.sub(r'[,]+', ',', text)
        text = re.sub(r'[ ]+', ' ', text)
        splittedText = text.split(' ')
        return self.parseList(splittedText)


    def parseList(self, termList):
        termList = list(filter(self.filterAll, termList))

        finalTermList = []

        for term in termList:
            if any(char.isdigit() for char in term):
                continue
            term = term.lower()
            if '-' in term:
                finalTermList += self.parseList(term.split('-'))
            elif ',' in term :
                finalTermList += self.parseList(term.split(','))
            elif '.' in term :
                finalTermList += self.parseList(term.split('.'))

            finalTermList.append(term)

        return finalTermList





class MySentences(object):
    def __init__(self, dirname, stopwordPath:str):
        self.dirname = dirname
        try:
            self.tokenizer = MyEmbedderTokenizer(stopwordPath)
        except AttributeError as err:
            pass

    def __iter__(self):
        counter = 0
        filesList = os.listdir(self.dirname)
        for fname in filesList:
            with open(os.path.join(self.dirname, fname)) as file:
                counter += 1
                if counter % 50000 == 0:
                    print (str(counter) + '/' + str(filesList) + "files processed")

                text = file.read()
                onlyText = getTagFromText(text, "<TEXT>", "</TEXT>")
                findTextSquared = onlyText.find('[Text]')
                if findTextSquared > 0:
                    onlyText = onlyText[findTextSquared + len('[Text]'):]
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
        start = datetime.now()
        sentences = MySentences(self._corpusPath, self._stopwordsPath)  # a memory-friendly iterator

        model = gensim.models.Word2Vec(sentences, min_count=1)
        model.save(self._outputPath)  # TODO set the path to where you want to save it
        finish = datetime.now()
        print("took: ", str((start - finish).seconds))
        return model


class WordEmbeddingUser(EmbeddingCreator):

    def __init__(self, modelPath:str, corpusPath:str=''):
        super(WordEmbeddingUser, self).__init__(corpusPath=corpusPath,outputPath=modelPath)
        self._modelPath = modelPath
        self._model = None

    def setModelPath(self, path:str):
        self._modelPath = path

    def loadModel(self):
        try:
            self._model = gensim.models.Word2Vec.load(self._modelPath)
        except Exception as err:
            print (err)
            return None

    def getModel(self)->gensim.models.Word2Vec:
        return self._model

    def getTopNSimilarWords(self, word:str ,N:int=5):
        try:
            self._model.most_similar(positive=[word], topn=N)
        except Exception as err:
            print (err)
            return None

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






# print (model)


# model = gensim.models.Word2Vec.load('../../test/word2vecTest2.txt')
# model.build_vocab(sentences=sentences,update=True)
# print('loaded the glove file to model')
# model.save('../../test/mymodel')
# print('saved the glove file to model')
# model = gensim.models.Word2Vec.load('../../test/mymodel')
# print('loaded the model file to model')
# model.train(sentences)
# print('trained the model on corpus')
#
# visualizeMyModel(model)
