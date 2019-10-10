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
@app.route('/tasks')
def render_tasks_table():
    tasks_order = list(mongo.db.task_importance.find())
    imp_order = {
        item.get('tsk_importance'): item.get('order') for item in tasks_order}
    
    return render_template('tasks_table.html',
                           tasks=mongo.db.tasks.find(
                               {'tsk_status': {'$ne': 'Completed'}}),
                           statuses=mongo.db.task_status.find(),
                           imp_order=imp_order, )


@app.route('/completed-tasks')
def render_completed_tasks_table():
    tasks_order = list(mongo.db.task_importance.find())
    imp_order = {
        item.get('tsk_importance'): item.get('order') for item in tasks_order}
    
    return render_template('completed_tasks_table.html',
                           tasks=mongo.db.tasks.find(
                               {'tsk_status': 'Completed'}),
                           imp_order=imp_order, )


@app.route('/add-task')
def render_add_task():
    return render_template('add_task.html',
                           categories=mongo.db.task_category.find(),
                           statuses=mongo.db.task_status.find(),
                           importances=mongo.db.task_importance.find())


@app.route('/insert-new-task', methods=['POST', ])
def insert_new_task():
    tasks = mongo.db.tasks
    form_res = request.form.to_dict()
    
    # Set default items if left empty
    if not form_res.get('tsk_category'):
        form_res['tsk_category'] = 'Undefined'
    
    if not form_res.get('tsk_status'):
        form_res['tsk_status'] = 'Not started'
    
    if not form_res.get('tsk_importance'):
        form_res['tsk_importance'] = 'Low'
    
    task_to_add = {
        'tsk_name': form_res.get('tsk_name'),
        'tsk_category': form_res.get('tsk_category'),
        'tsk_status': form_res.get('tsk_status'),
        'tsk_description': form_res.get('tsk_description'),
        'tsk_due_date': form_res.get('tsk_due_date'),
        'tsk_importance': form_res.get('tsk_importance'),
        'tsk_issue': False,
    }
    tasks.insert_one(task_to_add)
    
    return redirect(url_for('render_tasks_table'))


@app.route('/edit-task/<task_id>')
def render_edit_task(task_id):
    task = mongo.db.tasks.find_one_or_404({'_id': ObjectId(task_id)})
    
    return render_template('edit_task.html',
                           task=task,
                           categories=mongo.db.task_category.find(),
                           statuses=mongo.db.task_status.find(),
                           importances=mongo.db.task_importance.find(),
                           )


@app.route('/update-task/<task_id>', methods=['POST', ])
def update_task(task_id):
    tasks = mongo.db.tasks
    task = mongo.db.tasks.find_one_or_404({'_id': ObjectId(task_id)})
    tasks.update_one({'_id': ObjectId(task_id)},
                     {'$set': {
                         'tsk_name': request.form.get('tsk_name'),
                         'tsk_category': request.form.get('tsk_category'),
                         'tsk_status': request.form.get('tsk_status'),
                         'tsk_description': request.form.get('tsk_description'),
                         'tsk_due_date': request.form.get('tsk_due_date'),
                         'tsk_importance': request.form.get('tsk_importance'),
                         'tsk_issue': task.get('tsk_issue'),
                     }}
                     )
    
    return redirect(url_for('render_tasks_table'))


@app.route('/toggle-issue-sign', methods=['POST', ])
def toggle_issue_sign():
    task_id = request.form.get('taskId')
    task = mongo.db.tasks.find_one_or_404({'_id': ObjectId(task_id)})
    if task.get('tsk_issue'):
        mongo.db.tasks.update_one({'_id': ObjectId(task_id)},
                                  {'$set': {'tsk_issue': False}})
    else:
        mongo.db.tasks.update_one({'_id': ObjectId(task_id)},
                                  {'$set': {'tsk_issue': True}})
    
    return redirect(url_for('render_tasks_table'))


@app.route('/edit-status', methods=['POST', ])
def edit_status():
    task_id = request.form.get('taskId')
    task_status = request.form.get('tsk_status')
    if task_status == 'Completed':
        timestamp = datetime.datetime.utcnow().strftime('%b %d, %Y')
        mongo.db.tasks.update_one({'_id': ObjectId(task_id)},
                                  {'$set': {
                                            'tsk_completed_date': timestamp,
                                            'tsk_status': task_status,
                                            }
                                   })
    else:
        mongo.db.tasks.update_one({'_id': ObjectId(task_id)},
                                  {'$set': {'tsk_status': task_status, }})
    
    return redirect(url_for('render_tasks_table'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
