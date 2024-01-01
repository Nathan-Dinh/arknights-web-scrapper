# Author: Nathan Dinh
# Revision: December 31 2023 - Nathan Dinh 

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import dotenv_values

#region Configuration 
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
#endregion

#region Schema
class OperatorInformationSchema:
    def __init__(self,imageUrl,name,profession,position,attackType,operatorTags,operatorArc,operatorProfile):
        self.imageUrl = str(imageUrl)
        self.name = str(name).strip().lower()
        self.profession = str(profession).strip().lower()
        self.operatorArc = str(operatorArc).strip()
        self.position = str(position).strip().lower()
        self.attackType = str(attackType).strip().lower()
        self.operatorTags = operatorTags
        self.operatorProfile = str(operatorProfile)

class SkinInformationSchema:
    def __init__(self,imageUrl,skinName,operatorName):
        self.imageUrl = str(imageUrl)
        self.skinName = str(skinName).strip().lower()
        self.operatorName = str(operatorName).strip().lower()
#endregion

#region Methods
def save_operator(operatorTemplate):
    try:
        postBody = {"imgUrl":operatorTemplate.imageUrl, 
                  "name": operatorTemplate.name,
                  "profession": operatorTemplate.profession,
                  "archetype": operatorTemplate.operatorArc,
                  "position": operatorTemplate.position,
                  "attackType": operatorTemplate.attackType,
                  "recruitmentTag": operatorTemplate.operatorTags,
                  "profile": operatorTemplate.operatorProfile}
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
        operatorName = htmlContext.find(class_="views-field views-field-field-skin-operator").a.get_text()
        #Sends another request using the url retrieved from the html context
        req = requests.get(config['DOMAIN_NAME'] + htmlContext.a['href'])
        ctx = BeautifulSoup(req.content, "html.parser")
        
        imageLink = ctx.find(id="image-tab-1").a['href']
        skinName = ctx.find(id="page-title").h1.get_text()
        return SkinInformationSchema(imageLink,skinName,operatorName)
    except Exception as e:
           raise ValueError(str(operatorName))

def get_operator_information(htmlContext):
        try:
            operatorName = htmlContext.find(id="page-title").h1.get_text()
            operatorImage = htmlContext.find(id="image-tab-1").a['href']
            #The operatorTags will return an array of tags
            operatorTags = htmlContext.find_all(class_="tag-title") 
            
            #This will loop through what is returned in the operators tags  
            for t in range(len(operatorTags)) :
                operatorTags[t] = operatorTags[t].get_text()
                if t == len(operatorTags) - 1 :
                    operatorArc = operatorTags[t].strip()
                    operatorTags.pop(len(operatorTags) - 1)
                    break
                operatorTags[t] = operatorTags[t].strip().lower()
                    
            operatorProfession = htmlContext.find(class_='profession-title').get_text()
            operatorPosition = htmlContext.find(class_='position-cell').a.get_text()
            operatorAttackType = htmlContext.find(class_="traits-cell").a.get_text()
            operatorProfile = htmlContext.find_all(class_='profile-description')
            operatorProfile = operatorProfile[0].get_text()

            return  OperatorInformationSchema(
                operatorImage,
                operatorName,
                operatorProfession,
                operatorPosition,
                operatorAttackType,
                operatorTags, 
                operatorArc,
                operatorProfile
            )
        except Exception as e:
           raise ValueError(str(operatorName))
#endregion

#region Operators
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
#endregion

#region Skins
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
#endregion