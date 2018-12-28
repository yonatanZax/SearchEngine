
import os
import re
import gensim

from Parsing.IterativeParsing import IterativeTokenizer
from BasicMethods import getTagFromText
from datetime import datetime



class MyEmbedderTokenizer(IterativeTokenizer):

    def __init__(self):
        try:
            super().__init__(None)
        except AttributeError as err:
            pass
        stopWordPath = '../../test/stop_words.txt'
        self.stopWordsDic = {}

        try:
            import os
            path = stopWordPath
            with open(path) as f:
                for word in f.read().splitlines():
                    self.stopWordsDic[word] = 'a'
                del self.stopWordsDic["may"]
        except IOError:
            print("Can't find path:", path)

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
    def __init__(self, dirname):
        self.dirname = dirname
        try:
            self.tokenizer = MyEmbedderTokenizer()
        except AttributeError as err:
            pass

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            with open(os.path.join(self.dirname, fname)) as file:
                text = file.read()
                onlyText = getTagFromText(text, "<TEXT>", "</TEXT>")
                findTextSquared = onlyText.find('[Text]')
                if findTextSquared > 0:
                    onlyText = onlyText[findTextSquared + len('[Text]'):]
                yield self.tokenizer.parseText(onlyText)



def visualizeMyModel(model):
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

    for word, pos in df.iterrows():
        ax.annotate(word, pos)
    plt.show()

start = datetime.now()
sentences = MySentences('../../test/FBIS3-99') # a memory-friendly iterator # TODO set the correct path


model = gensim.models.Word2Vec(sentences, min_count=1)
model.save('../../test/mymodel') # TODO set the path to where you want to save it
finish = datetime.now()
print("took: ", str((start-finish).seconds))
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
