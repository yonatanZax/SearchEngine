from nltk.stem import PorterStemmer
from nltk.stem import snowball

# ps = PorterStemmer(PorterStemmer.NLTK_EXTENSIONS)
ps = snowball.SnowballStemmer("english")

def stemTerm(termAsString):
    afterStem = ps.stem(termAsString)
    if termAsString[0].isupper():
        afterStem = afterStem[0].upper() + afterStem[1:]
    # if afterStem[0] == termAsString[0].lower:
    #     if afterStem[0] != termAsString[0]:
    #         afterStem[0] = termAsString[0]
    return afterStem


