from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
import re
import csv
#legend nur für Bundesland 1 Wahlkreis 1 Richtig
legend=["Bundesland", "Wahlkreis", "Wahlberechtigte Anzahl", "Wähler Anzahl" , "Ungültige Anzahl", "Gültige Anzahl", "CDU Anzahl", "SPD Anzahl", "Grüne Anzahl", "FDP Anzahl", "Linke Anzahl", "AfD Anzahl", "NPD Anzahl", "Freie Wähler Anzahl", "MLPD Anzahl", "BGE Anzahl", "ÖDP Anzahl", "Die PARTEI Anzahl", "EB: KrügerWinands Anzahl", "Tierschutzpartei Anzahl", "PIRATEN Anzahl", "Übrige Anzahl"]

def main():
    with open("data.csv", "w+") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(legend)
    myfile.close()
    land = 1
    wahlkreis = 1
    toomany = 0
    while(wahlkreis<300):
        toomany+=1
        try:
            getpage = requests.get("https://www.bundeswahlleiter.de/bundestagswahlen/2017/ergebnisse/bund-99/land-%d/wahlkreis-%d.html" % (land, wahlkreis))
            getpage.raise_for_status()
        except HTTPError:
            #print("Wahlkreis %d in Bundesland %d existiert nicht" %(wahlkreis, land))
            land+=1
            if land==17:
                land = 1
            continue
        else:
            page = getpage.content
            GetData(BeautifulSoup(page, "lxml"), land, wahlkreis)
            print ("Wahlkreis %d in Bundesland %d hinzugefuegt" %(wahlkreis, land))
            wahlkreis+=1
        if toomany>2000:
            print("Too many")
            break
    print(toomany)
    return
	
def GetData(soup, land, wahlkreis):
    first_block = soup.find_all('tbody')[0]
    second_block = soup.find_all('tbody')[1]
    ErststimmenAnzahl = []
    ErststimmenProzent = []
    ErststimmenDifferenz = []
    ZweitstimmenAnzahl = []
    ZweitstimmenProzent = []
    ZweitstimmenDifferenz = []
    for row in first_block.find_all('tr'):
        cells1 = row.find_all(class_='colgroup-1 align--right')
        cells2 = row.find_all(class_='colgroup-2 align--right')
        ErststimmenAnzahl.append(cells1[0].find(text=True))
        ErststimmenProzent.append(cells1[1].find(text=True))
        ErststimmenDifferenz.append(cells1[2].find(text=True))
        ZweitstimmenAnzahl.append(cells2[0].find(text=True))
        ZweitstimmenProzent.append(cells2[1].find(text=True))
        ZweitstimmenDifferenz.append(cells2[2].find(text=True)) 
    #gleiche nochmal für den zweiten block
    for row in second_block.find_all('tr'):
        cells1 = row.find_all(class_='colgroup-1 align--right')
        cells2 = row.find_all(class_='colgroup-2 align--right')
        ErststimmenAnzahl.append(cells1[0].get_text())
        ErststimmenProzent.append(cells1[1].find(text=True))
        ErststimmenDifferenz.append(cells1[2].find(text=True))
        ZweitstimmenAnzahl.append(cells2[0].find(text=True))
        ZweitstimmenProzent.append(cells2[1].find(text=True))
        ZweitstimmenDifferenz.append(cells2[2].find(text=True))
    ErststimmenAnzahl = FormatColumnIntData(ErststimmenAnzahl)
    ErststimmenProzent = FormatColumnFloData(ErststimmenProzent)
    ErststimmenDifferenz = FormatColumnFloData(ErststimmenDifferenz)
    ZweitstimmenAnzahl = FormatColumnIntData(ZweitstimmenAnzahl)
    ZweitstimmenProzent = FormatColumnFloData(ZweitstimmenProzent)
    ZweitstimmenDifferenz = FormatColumnFloData(ZweitstimmenDifferenz)
    wahlkreisResults = []
    wahlkreisResults.append(land)
    wahlkreisResults.append(wahlkreis)
    wahlkreisResults = wahlkreisResults + ErststimmenAnzahl + ErststimmenProzent + ErststimmenDifferenz + ZweitstimmenAnzahl + ZweitstimmenProzent + ZweitstimmenDifferenz
    AddRowCSV(wahlkreisResults)
    return 
        
#Bekommt Spalte (Liste) wie ErststimmenAnzahl und macht Liste aus INTEGERS 
def FormatColumnIntData(column = []):
    newcolumn = []
    for el in range(len(column)):
        tempvar = re.findall(r'\d+.\d+', column[el])
        if tempvar:
            tempvar = tempvar[0]
            tempvar = tempvar.replace(".","")
            newcolumn.append(int(tempvar))
        else:
            newcolumn.append(None)
    return newcolumn

#Bekommt Spalte (Liste) wie ErststimmenProzent und macht Liste aus Floats 
def FormatColumnFloData(column = []):
    newcolumn = []
    for el in range(len(column)):
        #tempvar = re.findall(r'\d+.\d+', column[el])
        tempvar = re.findall(r'-?\d+.\d+', column[el])
        if tempvar:
            tempvar = tempvar[0]
            tempvar = tempvar.replace(",",".")
            newcolumn.append(float(tempvar))
        else:
            newcolumn.append(None)
    return newcolumn

def AddRowCSV(mylist = []):
    with open("data.csv", 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(mylist)
    return

if __name__ == '__main__':
    main()