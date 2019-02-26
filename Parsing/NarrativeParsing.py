import re
import lxml.html


narrStopWords = ["purposes","refer","refers","include","prescribed","issues","must","contain","discuss","discussing","considered","relevant","document","documents"]


def parseText(text, stopWordsDic):


    for w in narrStopWords:
        stopWordsDic[w] = True


    t = lxml.html.fromstring(text)
    text = t.text_content()

    text = text.replace("'s", '').replace("\n", ' ').replace('\t', ' ').replace('{', ' ').replace('}', ' ').replace('[',
                                                                                                                    ' ').replace(
        ']',
        ' ').replace(
        '\"', ' ').replace('\'', ' ').replace('(', ' ').replace(')', ' ').replace('?', ' ').replace('!', ' ').replace(
        '#',
        ' ').replace(
        '@', ' ').replace('/', ' ').replace('\\', ' ').replace('_', ' ').replace('>', ' ').replace('<', ' ').replace(
        '`',
        ' ').replace(
        '~', ' ').replace(';', ' ').replace(':', ' ').replace('*', ' ').replace('+', ' ').replace('|', ' ').replace('&',
                                                                                                                    ' ').replace(
        '=', ' ')
    text = re.sub(r'[-]+', '-', text)
    text = re.sub(r'[.]+', '', text)
    text = re.sub(r'[,]+', '', text)
    text = re.sub(r'[ ]+', ' ', text)
    splittedText = text.split(' ')


    finalList = set()


    for t in splittedText:

        if stopWordsDic.get(t.lower()) is None:
            finalList.add(t)


    return list(finalList)








def getNarrWithRegex(narrText,stopWords):

    narrText = re.sub(r'\([^)]*\)', ' ', narrText)

    pattern0 = re.compile(r"Documents discussing the following issues are relevant:[- \w\n\t]*Documents")
    match0 = pattern0.findall(narrText)


    if len(match0) > 0 and match0[0].count(" - ") > 0:
        match0 = match0[0].split(" - ")


    pattern1 = re.compile(r"[Dd]ocument[- \w\n]*relevant.")
    match1 = pattern1.findall(narrText)

    pattern2 = re.compile(r"A relevant document[- \w\n]*.")
    match2 = pattern2.findall(narrText)

    pattern3 = re.compile(r"Relevant document[- \w\n]*.")
    match3 = pattern3.findall(narrText)

    matchList = match0 + match1 + match2 + match3

    totalList = []
    for match in matchList:

        textToParse = match
        if "not relevant" in textToParse or "non-relevant" in textToParse:
            continue
        totalList += parseText(textToParse,stopWords)

    return totalList

