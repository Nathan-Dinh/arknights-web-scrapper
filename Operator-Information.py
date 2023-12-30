# Author: Nathan Dinh
# Revision: December 29 2023 - Nathan Dinh 

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import dotenv_values

# Imports all variables from .env file 
config = {**dotenv_values("./config/.env.secret")}
# Connect your application to your database
client = MongoClient(config['MONGODB_CONNECTION_STRING'])
database = client[config['DATABASE_NAME']]
operatorCollection = database[config['OPERATORS_COLLECTION']]
skinCollection = database[config['SKINS_COLLECTION']]

# Collection constraints
operatorCollection.create_index('name', unique=True)
skinCollection.create_index('skinName', unique=True)

# Operate class
class OperatorInformationTemplate:
    def __init__(self,imageUrl,name,operatorTags,operatorArc,operatorProfile):
        self.imageUrl = str(imageUrl)
        self.name = str(name)
        self.operatorTags = operatorTags
        self.operatorArc = str(operatorArc)
        self.operatorProfile = str(operatorProfile)

class SkinInformationTemplate:
    def __init__(self,imageUrl,skinName,operatorName):
        self.imageUrl = str(imageUrl)
        self.skinName = str(skinName)
        self.operatorName = str(operatorName)

# Method will save the operators information to your database
def save_operator(operatorTemplate):
    try:
        postBody = {"imgUrl":operatorTemplate.imageUrl, 
                  "name": operatorTemplate.name,
                  "recruitmentTag": operatorTemplate.operatorTags,
                  "archetype": operatorTemplate.operatorArc,
                  "profile": operatorTemplate.operatorProfile,}
        operatorCollection.insert_one(postBody)
        print(operatorTemplate.name + ":Saved")
    except Exception as e:
        print(str(e))
    return

def save_skin(skinTemplate):
    try:
        postBody = {"imgUrl":skinTemplate.imageUrl, 
                  "skinName": skinTemplate.skinName,
                  "operatorName": skinTemplate.operatorName}
        skinCollection.insert_one(postBody)
        print(skinTemplate.skinName + ":Saved")
    except Exception as e:
        print(str(e))
    return

def get_skin_information(htmlContext):
    try:
        operatorName = htmlContext.find(class_="views-field views-field-field-skin-operator").a.get_text().lower()
        skinLink = htmlContext.a['href']
        req = requests.get(config['DOMAIN_NAME']+skinLink)
        ctx = BeautifulSoup(req.content, "html.parser")
        imageLink = ctx.find(id="image-tab-1").a['href']
        skinName = ctx.find(id="page-title").h1.get_text().lower()
        return SkinInformationTemplate(imageLink,skinName,operatorName)
    except Exception as e:
           print(e)
           raise ValueError(str(operatorName))

def get_operator_information(htmlContext):
        try:
            operatorImage = htmlContext.find(id="image-tab-1").a['href']
            operatorName = htmlContext.find(id="page-title").h1.get_text().lower()
            operatorTags = htmlContext.find_all(class_="tag-title")
            operatorProfile = htmlContext.find_all(class_='profile-description')

            for t in range(len(operatorTags)) :
                operatorTags[t] = operatorTags[t].get_text().strip()

            if t == len(operatorTags) - 1 :
                operatorArc = operatorTags[t]
                operatorTags.pop(len(operatorTags) - 1)

            return  OperatorInformationTemplate(operatorImage,operatorName,operatorTags, operatorArc,operatorProfile[0].get_text())
        except Exception as e:
           print(e)
           raise ValueError(str(operatorName))

reqOperatorListPage = requests.get(config['DOMAIN_NAME'] + config['OPERATOR_LIST_URL'])
ctxOperatorListHtml = BeautifulSoup(reqOperatorListPage.content, "html.parser")
operatorUrls = ctxOperatorListHtml.find_all(class_='operator-title-actual') # Collects the operators url 

for link in operatorUrls :
    req = requests.get(config['DOMAIN_NAME'] + link['href'])
    operatorProfilePage = BeautifulSoup(req.content, "html.parser")
    try:
        save_operator(get_operator_information(operatorProfilePage))
    except ValueError as e:
        print(str(e) + ": Could not be saved")
    break

reqSkinListPage = requests.get(config['DOMAIN_NAME'] + config['SKIN_LIST_URL'])
ctxSkinListHtml = BeautifulSoup(reqSkinListPage.content, "html.parser")
ctxSkinListHtml = ctxSkinListHtml.find(id="topic-511941")
ctxSkinListHtml = ctxSkinListHtml.find('tbody')
tableRows = ctxSkinListHtml.find_all('tr')

for row in tableRows:
    try:
        save_skin(get_skin_information(row))
    except ValueError as e:
        print(str(e) + ": Could not be saved")
    break