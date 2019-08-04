import os
from flask import Flask
from flask_pymongo import PyMongo
import bson
#from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)


@app.route('/')
def test_mongodbs():
    test_coll = mongo.db.testcollection.find()
    return str([doc for doc in test_coll])
    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)