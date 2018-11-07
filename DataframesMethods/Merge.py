

from DataframesMethods import BasicDF




def test():
    import pandas as pd
    dfA = BasicDF.createDataFrameByColumns(['Term','Sum','Posting'],[['act','apple','airplane'],[3,6,10],['F1-121,','F1-223,','F2-51,']])
    dfA.set_index('Term',inplace=True)
    print('\nDataframe A')
    print(dfA)
    dfB = BasicDF.createDataFrameByColumns(['Term','Sum','Posting'],[['act','apple','airplane'],[3,2,10],['F1-11,','F3-13,','F2-54,']])
    dfB.set_index('Term',inplace=True)
    print('\nDataframe A')
    print(dfB)

    dfC = BasicDF.createDataFrameByColumns(['Term','Sum','Posting'],[['apple','act','airplane'],[3,2,10],['F1-11,','F3-13,','F2-54,']])
    dfD = BasicDF.createDataFrameByColumns(['Term','Sum','Posting'],[['apple','act','airplane'],[3,2,10],['F1-11,','F3-13,','F2-54,']])
    dfE = BasicDF.createDataFrameByColumns(['Term','Sum','Posting'],[['apple','act','airplane'],[3,2,10],['F1-11,','F3-13,','F2-54,']])

    dfA = dfA.add(dfB, fill_value=0)

    dfC = dfC.add(dfD, fill_value=0)
    dfNew = dfA.add(dfC, fill_value=0)
    dfNew = dfNew.add(dfE, fill_value=0)


    print('\nDataframe A+B')
    print(dfNew)

test()






