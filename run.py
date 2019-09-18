import bson
from bson.objectid import ObjectId
import datetime
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
import os


app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)


@app.route('/')
def render_home_page():
    return render_template('base.html')


@app.route('/tasks')
def render_tasks_table():
    return render_template('tasks_table.html', 
        tasks=mongo.db.tasks.find({'$or': [{'end_timestamp': ""}, 
                                  {'end_timestamp': None}]}))


@app.route('/tasks-done')
def render_tasks_done_table():
    return render_template('tasks_done_table.html', 
        tasks=mongo.db.tasks.find({'$nor': [{'end_timestamp': ""}, 
                                  {'end_timestamp': None}]}))


@app.route('/add_task')
def render_add_task():
    return render_template('add_task.html',
                           categories=mongo.db.task_category.find(),
                           statuses=mongo.db.task_status.find(),
                           importances=mongo.db.task_importance.find())


@app.route('/insert_new_task', methods=['POST', ])
def insert_new_task():
    tasks = mongo.db.tasks
    print(request.form.to_dict())
    tasks.insert_one(request.form.to_dict())
    
    return redirect(url_for('render_tasks_table'))


@app.route('/edit_task/<task_id>')
def render_edit_task(task_id):
    task = mongo.db.tasks.find_one_or_404({'_id': ObjectId(task_id)})
    print('\ntask', task)
    
    return render_template('edit_task.html',
                           task=task,
                           categories=mongo.db.task_category.find(),
                           statuses=mongo.db.task_status.find(),
                           importances=mongo.db.task_importance.find())


@app.route('/update_task/<task_id>', methods=['POST',])
def update_task(task_id):
    tasks = mongo.db.tasks
    task = mongo.db.tasks.find_one_or_404({'_id': ObjectId(task_id)})
    tasks.update_one({'_id': ObjectId(task_id)},
                     {'$set': {
                         'name': request.form.get('name'),
                         'category': request.form.get('category'),
                         'description': request.form.get('description'),
                         'status': request.form.get('status'),
                         'importance': request.form.get('importance'),
                         'due_date': request.form.get('due_date'),
                         'notes': task.get('notes'),
                     }})
    
    return redirect(url_for('render_tasks_table'))


@app.route('/toggle-issue-sign', methods=['POST', ])
def toggle_issue_sign():
    task_id = request.form.get('taskId')
    task = mongo.db.tasks.find_one_or_404({'_id': ObjectId(task_id)})
    if task.get('issue'):
        mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, 
            {'$set': {'issue': False}})
    else:
        mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, 
            {'$set': {'issue': True}})
    
    return redirect(url_for('render_tasks_table'))


@app.route('/mark-task-done', methods=['POST', ])
def mark_task_done():
    task_id = request.form.get('taskId')
    res = mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, 
        {'$set': {'completed_date': datetime.datetime.utcnow().strftime('%b %d, %Y')}})
    print('mark task as completed', res.raw_result)
    
    return redirect(url_for('render_tasks_table'))    



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
