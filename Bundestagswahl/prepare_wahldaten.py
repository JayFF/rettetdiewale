import pandas as pd
import re
import numpy as np

def strukturdaten(filename, seperator=";"):
    data = pd.read_csv(filename, seperator, encoding='latin1', skiprows=[0,1,2,3,4,5,6,7])
    return(data)

def wahlergebnis(filename, seperator=";"):
    data = pd.read_csv("btw17_kerg.csv",";",skiprows=[0,1,2,3,4])
    data2 = data.drop([column for column in list(data) if (
                        re.search("Unnamed:.*", column) and "Zweitstimmen" not in list(data[column]))],
                                                                                                axis=1)

    for index, column in enumerate(list(data2)):
        if re.match("Unnamed: .*", column):
            #print((str(list(data)[index])+" Zweitstimmen"+str(index)))
            data2 = data2.rename(columns={column: (str(list(data2)[index-1])+"Zweitstimmen")})
            data2 = data2.rename(columns={list(data2)[index-1]: (str(list(data2)[index-1])+"Erststimmen")})
    
    data2.drop(data2.index[0], inplace=True)
    data2 = data2.reset_index()
    data2 = data2.drop(["index"], axis=1)
    data2 = data2.drop([index for index in list(data2.index) if (data2.isnull().iloc[index][1] == True)])

    return(data2)
