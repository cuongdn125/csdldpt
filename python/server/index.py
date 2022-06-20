from cmath import sqrt
from xml.sax.handler import all_features
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
import base64
import numpy as np
import random
import cv2
import collections
import json
# creating a Flask app
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
client = MongoClient('localhost', 27017)
db = client.flask_db

feature = db.feature

@app.route('/', methods = [ 'POST'])
def home():
    data = request.get_json()
    b64 = data["content"]
    starter = b64.find(',')
    image_data = b64[starter+1:]
    image_data = bytes(image_data, encoding="ascii")
    name = str(random.random())
    # fruits = ["Apple", "Apricot", "Cantaloupe","Chestnut","Cocos","Guava","Kumquats","Lemon","Limes","Lychee","Mandarine","Onion White","Orange","Peach","Pear","Plum","Pomegranate","Potato White","Tomato","Watermelon"]
    # for fruit in fruits:
        # print(fruit)
        # for p in range(50):
        #     url = "./fruits-360/Training/"+fruit+"/anh (" + str(p+1) + ").jpg"
    url = "./test/img/" + name+".jpeg"
        # print(url)
    with open(url, 'wb') as fh:
        fh.write(base64.b64decode(image_data))

    img = cv2.imread(url)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = []
    colorsFeature = [255,245,190,133,69,0,190, 180, 161,147,84,232, 210,224,179,29,15,134,123,141,210,193,164,150,59,237,226,202,173,140,151,76,59,42,236,212,105,105,102,57]
    result = []
    for i in range(5):
        for j in range(5):
            matrix = gray[i*20:(i+1)*20, j*20:(j+1)*20]
            x=[]
            for n in range(40):
                count=0
                for k in range(20):
                    for l in range(20):
                        if matrix[k][l] < colorsFeature[n] +2 and matrix[k][l]> colorsFeature[n]-2:
                            count += 1
                x.append(count)
            result.append(x)



    # feature.insert_one({"name":fruit+str(p+1), "feature":result, "class": fruit})
    data = feature.find()
    # # print(a[0])
    d =[]
    for doc in data:
        d1=0
        for i in range(len(doc["feature"])):
            d2=0
            for j in range(len(doc["feature"][i])):
                d2 += pow(doc["feature"][i][j] - result[i][j], 2)
            d1 +=sqrt(d2)
        d.append({"name":doc["name"], "distance":d1.real, "class":doc["class"]})
    d.sort(key=lambda x: x["distance"])
    c = collections.Counter(doc["class"] for doc in d[:13])
    print(c)

    return (jsonify({"class":c.most_common()[0][0]}))

    # return ("ok")






# driver function
if __name__ == '__main__':

	app.run(debug = True)
