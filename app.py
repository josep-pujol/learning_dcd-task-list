import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
import bson
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)


@app.route('/')
def test():
    return render_template('base.html')


@app.route('/tasks')
def render_tasks_table():
    return render_template('tasks_table.html', tasks=mongo.db.tasks.find())


@app.route('/issue_sign/<task_id>')
def issue_sign(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    return redirect(url_for('render_tasks_table'))


@app.route('/toggle_issue_sign/<task_id>', methods=['POST', ])
def toggle_issue_sign(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    if task.issue == 'issue':
        res = mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'issue': 'no'}})
    else:
        res = mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'issue': 'issue'}})
    print('toggled issue sign', res)
    return redirect(url_for('render_tasks_table'))


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


@app.route('/edit_task/<task_id>')
def render_edit_task(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    print('\ntask', task)
    return render_template('edit_task.html',
                           task=task,
                           categories=mongo.db.task_category.find(),
                           statuses=mongo.db.task_status.find(),
                           importances=mongo.db.task_importance.find())


@app.route('/update_task/<task_id>', methods=['POST',])
def update_task(task_id):
    tasks = mongo.db.tasks
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    tasks.update({'_id': ObjectId(task_id)},
                 {'name': request.form.get('name'),
                  'category': request.form.get('category'),
                  'description': request.form.get('description'),
                  'status': request.form.get('status'),
                  'importance': request.form.get('importance'),
                  'due_date': request.form.get('due_date'),
                  'start_timestamp': task.get('start_timestamp'),
                  'end_timestamp': task.get('end_timestamp'),
                  'notes': task.get('notes'),
                  })
    return redirect(url_for('render_tasks_table'))



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
