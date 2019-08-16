import os
from flask import Flask, render_template
from flask_pymongo import PyMongo
import bson
#from bson.objectid import ObjectId


app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)


@app.route('/')
def test():
    return render_template('base.html')


@app.route('/tasks')
def render_tasks_table():
    return render_template('tasks_table.html', tasks=mongo.db.tasks.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)