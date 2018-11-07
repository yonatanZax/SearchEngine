from nltk.stem import PorterStemmer

ps = PorterStemmer(PorterStemmer.NLTK_EXTENSIONS)


def stemTerm(termAsString):
    return ps.stem(termAsString)


