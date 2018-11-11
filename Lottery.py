#!/usr/bin/env python
# coding: utf-8

# In[123]:


import requests
import json
import codecs
import pathlib


# In[124]:


def writeToFile(fileName, content) :
    print(fileName)
    output = open(fileName, 'w')
    output.write(content)


# In[125]:


def createLuckGameFolder(directoryName) :
    pathlib.Path(directoryName).mkdir(exist_ok=True) 


# In[126]:


# sayisal, sanstopu, onnumara, superloto
def getLuckGameDrawDates(gameName = "onnumara"):
    url = 'http://www.mpi.gov.tr/sonuclar/listCekilisleriTarihleri.php?tur=' + gameName
    resp = requests.get(url)
    writeToFile(gameName + '_draw_dates.json', resp.text);
    dataJson = json.load(codecs.open(gameName + '_draw_dates.json', 'r', 'utf-8-sig'))
    drawDates = []
    for drawDate in dataJson :
        #print(drawDate['tarih'])
        drawDates.append(drawDate['tarih'])
    print(gameName + ' toplam cekilis sayisi ' + str(len(drawDates)))
    return drawDates


# In[127]:


def fixResultJsonName(drawDate) :
    if(game == 'sayisal') :
        return 'SAY_' + drawDate
    else :
        return drawDate


# In[131]:


def getGameResult(game, drawDate) :
    url = 'http://www.mpi.gov.tr/sonuclar/cekilisler/' + game + '/' + fixResultJsonName(drawDate) + '.json'
    resp = requests.get(url=url)
    try:
        dataJson=resp.json()
        print(url)
    except ValueError:
        url = 'http://www.mpi.gov.tr/sonuclar/cekilisler/' + game + '/' + drawDate + '.json'
        print(url)
        resp = requests.get(url=url)
        dataJson = resp.json()

    if(dataJson['success']) :
        data = dataJson['data']
        writeToFile(game + '/' + drawDate + '.json', json.dumps(data))
        return data['rakamlar']
    else :
        print('WTH???')


# In[132]:


def getAllLotteryGameResult() :
    gameList = ('sayisal', 'sanstopu', 'onnumara', 'superloto')
    for game in gameList :
        createLuckGameFolder(game)
        drawDates = getLuckGameDrawDates(game)
        for drawDate in drawDates :
            result = getGameResult(game, drawDate)
            print(result)


# In[139]:


def getLastResults(game, atLeast = 1) :
    createLuckGameFolder(game)
    drawDates = getLuckGameDrawDates(game)
    for index in range(0, atLeast) :
        print(drawDates[index])
        
    
    




# In[141]:


getLastResults('superloto', 2)


# In[142]:


getLastResults('sanstopu')


# In[ ]:




