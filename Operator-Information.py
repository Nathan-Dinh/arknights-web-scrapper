# Author: Nathan Dinh
# Revision: December 20 2023 - Nathan Dinh 

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

DOMAIN_NAME_URL = str("https://gamepress.gg")
SUB_FOLDER_URL = str("/arknights/tools/interactive-operator-list#tags=null##stats")

# Mongodb connection string goes here example: mongodb+srv://[username:password@]host[/[defaultauthdb][?options]]
MONGODB_CONNECTION_STRING = str("<Connection string goes here>")

# Database and collection name
DATABASE_NAME = str("<mongodb database name goes here>")
COLLECTION_NAME = str("<collection name goes here>")

# Connect your application to your database
clu = MongoClient(MONGODB_CONNECTION_STRING)
db = clu[DATABASE_NAME]
collection = db[COLLECTION_NAME]

operatorId = 0;

# Operate class
class OperatorInformation:
    def __init__(self,id,imageUrl,name,operatorTags,operatorArc,operatorProfile):
        self.id = int(id)
        self.imageUrl = str(imageUrl)
        self.name = str(name)
        self.operatorTags = operatorTags
        self.operatorArc = str(operatorArc)
        self.operatorProfile = str(operatorProfile)

# Method will save the operators information to your database
def save_operator(operator):
    try:
        postBody = {"_id" : operator.id, 
                  "imgUrl":operator.imageUrl, 
                  "name": operator.name,
                  "recruitmentTag": operator.operatorTags,
                  "archetype": operator.operatorArc,
                  "profile": operator.operatorProfile,}
        collection.insert_one(postBody)
        print(operator.name + ":Saved")
    except Exception as e:
        print(str(e))

    return

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

            op = OperatorInformation(operatorId,operatorImage,operatorName,operatorTags, operatorArc,operatorProfile[0].get_text())
        except Exception as e:
           print(e)
           raise ValueError(str(operatorName))
        return op


req = requests.get(DOMAIN_NAME_URL + SUB_FOLDER_URL)
ctx = BeautifulSoup(req.content, "html.parser")

# Collects the operators url 
operatorLink = ctx.find_all(class_='operator-title-actual')

for o in operatorLink :
    req = requests.get(DOMAIN_NAME_URL + o['href'])
    ctx = BeautifulSoup(req.content, "html.parser")
    operatorId += 1
    
    try:
        operatorInformation = get_operator_information(ctx)
        save_operator(operatorInformation)
    except ValueError as e:
        print(str(e) + ": Could not be saved")
        

    
        
    





    