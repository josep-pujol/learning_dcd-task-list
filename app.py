import os
from flask import Flask, render_template, redirect, request, url_for
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


@app.route('/add_task')
def render_add_task():
    return render_template('add_task.html',
                           categories=mongo.db.task_category.find(),
                           statuses=mongo.db.task_status.find(),
                           importances=mongo.db.task_importance.find())


@app.route('/insert_new_task', methods=['POST', ])
def insert_new_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('render_tasks_table'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)