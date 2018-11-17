from nltk.stem import PorterStemmer

ps = PorterStemmer(PorterStemmer.NLTK_EXTENSIONS)


def stemTerm(termAsString):
    afterStem = ps.stem(termAsString)
    if afterStem[0] == termAsString[0].lower:
        if afterStem[0] != termAsString[0]:
            afterStem[0] = termAsString[0]
    return afterStem


