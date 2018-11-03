from nltk.stem import PorterStemmer

ps = PorterStemmer()


def stemTerm(termAsString):
    return ps.stem(termAsString)

