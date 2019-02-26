from nltk.stem import snowball

ps = snowball.SnowballStemmer("english")

def stemTerm(termAsString):
    afterStem = ps.stem(termAsString)
    if termAsString[0].isupper():
        afterStem = afterStem[0].upper() + afterStem[1:]

    return afterStem


