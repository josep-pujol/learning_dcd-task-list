from bson.objectid import ObjectId
import datetime
import time
from run import app, mongo
import unittest


existing_collections = ['task_importance', 'tasks', 'task_category', 
                        'task_status']
time_stamp_obj = datetime.datetime.utcnow()
dummy_task = {'tsk_name': 'Testing Task',
              'tsk_category': 'Undefined',
              'tsk_status': 'Not started',
              'tsk_description': 'Test Description' + str(time_stamp_obj),
              'tsk_due_date': time_stamp_obj.strftime('%b %d, %Y'),
              'tsk_importance': 'Low',
              'tsk_issue': False, }


class TestAppCase(unittest.TestCase):
    
    
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.dummy_task = dummy_task
    
    
    def tearDown(self):
        task_description = {
            'tsk_description': self.dummy_task['tsk_description']}
        dummy_tasks = mongo.db.tasks.count_documents(task_description)
        if dummy_tasks:
            mongo.db.tasks.delete_one(task_description)
    
    
    def test_collections_exist(self):
        collections = mongo.db.list_collection_names()
        for collection in collections:
            self.assertIn(collection, existing_collections)
    
    
    def test_render_home_page(self):
        res = self.client.get('/')
        res_text = res.get_data(as_text=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('"brand-logo">WFM', res_text)
    
    
    def test_render_tasks_table(self):
        res = self.client.get('/tasks')
        res_text = res.get_data(as_text=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('"section-title">Tasks', res_text)
    
    
    def test_render_completed_tasks(self):
        res = self.client.get('/completed-tasks')
        res_text = res.get_data(as_text=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('"section-title">Completed Tasks', res_text)
    
    
    def test_render_add_task(self):
        res = self.client.get('/add-task')
        res_text = res.get_data(as_text=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('"section-title">Add Task', res_text)
    
    
    def test_insert_new_task(self):
        res = self.client.post('/insert-new-task', 
                               data=self.dummy_task, 
                               follow_redirects=True)
        dummy_task_description = mongo.db.tasks.find(
            {'tsk_description': self.dummy_task['tsk_description']})
        
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(dummy_task_description)
    
    
    def test_render_edit_task(self):
        dummy_task_id = mongo.db.tasks.insert_one(self.dummy_task).inserted_id
        res = self.client.get(f'/edit-task/{dummy_task_id}',
                              follow_redirects=True)
        res_text = res.get_data(as_text=True)     
        
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.dummy_task['tsk_description'], res_text)        
    
    
    def test_update_task(self):
        dummy_task_id = mongo.db.tasks.insert_one(self.dummy_task).inserted_id
        self.dummy_task['name'] = 'Testing Update Task'
        res = self.client.post(f'/update-task/{dummy_task_id}',
                               data=self.dummy_task,
                               follow_redirects=True)
        updated_dummy_task = mongo.db.tasks.find_one(
                                    {'_id': ObjectId(dummy_task_id)})
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.dummy_task['tsk_name'], 
                         updated_dummy_task.get('tsk_name'))
    
    
    def test_toggle_issue_sign_add(self):
        dummy_task_id = mongo.db.tasks.insert_one(self.dummy_task).inserted_id
        data = {'taskId': dummy_task_id}
        res = self.client.post('/toggle-issue-sign',
                               data=data,
                               follow_redirects=True)
        dummy_task_issue = mongo.db.tasks.find_one(
                                    {'_id': ObjectId(dummy_task_id)})
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(dummy_task_issue.get('tsk_issue'))        
    
    
    def test_toggle_issue_sign_remove(self):
        dummy_task_id = mongo.db.tasks.insert_one(self.dummy_task).inserted_id
        data = {'taskId': dummy_task_id}
        mongo.db.tasks.update_one({'_id': ObjectId(dummy_task_id)}, 
                                  {'$set': {'tsk_issue': True}})
        res = self.client.post('/toggle-issue-sign',
                               data=data,
                               follow_redirects=True)
        dummy_task_no_issue = mongo.db.tasks.find_one(
                                    {'_id': ObjectId(dummy_task_id)})
        
        self.assertEqual(res.status_code, 200)
        self.assertFalse(dummy_task_no_issue.get('tsk_issue')) 
    
    
    def test_edit_status_not_completed(self):
        dummy_task_id = mongo.db.tasks.insert_one(self.dummy_task).inserted_id
        data = {'taskId': dummy_task_id,
                'tsk_status': '0%',
                }
        res = self.client.post('/edit-status',
                               data=data,
                               follow_redirects=True)
        dummy_task_zero_percent = mongo.db.tasks.find_one(
                                    {'_id': ObjectId(dummy_task_id)})
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(dummy_task_zero_percent.get('tsk_status'),
                         data.get('tsk_status')) 
    
    
    def test_edit_status_completed(self):
        dummy_task_id = mongo.db.tasks.insert_one(self.dummy_task).inserted_id
        data = {'taskId': dummy_task_id,
                'tsk_status': 'Completed',
                }
        res = self.client.post('/edit-status',
                               data=data,
                               follow_redirects=True)
        timestamp = datetime.datetime.utcnow().strftime('%b %d, %Y')
        dummy_task_completed = mongo.db.tasks.find_one(
                                    {'_id': ObjectId(dummy_task_id)})
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(dummy_task_completed.get('tsk_status'),
                         data.get('tsk_status'))
        self.assertEqual(dummy_task_completed.get('tsk_completed_date'),
                         timestamp)


if __name__ == '__main__':
    unittest.main()
