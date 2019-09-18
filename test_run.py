from bson.objectid import ObjectId
import datetime
import time
from run import app, mongo
import unittest
import json

existing_collections = ['task_importance', 'tasks', 'task_category', 
                        'task_status']

time_stamp_obj = datetime.datetime.utcnow()
dummy_task = {'name': 'Testing Task',
             'category': 'Test Category',
             'description': 'Test Description' + str(time_stamp_obj),
             'status': 'Test Status',
             'importance': 'Test Importance',
             'due_date': time_stamp_obj.strftime('%b %d, %Y'), }



class TestAppCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.dummy_task = dummy_task
    
    
    def tearDown(self):
        task_description = {'description': self.dummy_task['description']}
        dummy_tasks = mongo.db.tasks.count_documents(task_description)
        print(dummy_tasks)
        if dummy_tasks:
            res = mongo.db.tasks.delete_one(task_description)
            print(res)

    
    def test_collections_exist(self):
        collections = mongo.db.list_collection_names()
        for collection in collections:
            self.assertIn(collection, existing_collections)
    
    
    def test_render_home_page(self):
        res = self.client.get('/')
        res_text = res.get_data(as_text=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('"brand-logo">Logo', res_text)
    
    
    def test_render_tasks_table(self):
        res = self.client.get('/tasks')
        res_text = res.get_data(as_text=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('"section-title">Tasks', res_text)
    
    
    def test_render_tasks_done_table(self):
        res = self.client.get('/tasks-done')
        res_text = res.get_data(as_text=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('"section-title">Completed Tasks', res_text)
    
    
    def test_render_add_task(self):
        res = self.client.get('/add_task')
        res_text = res.get_data(as_text=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('"section-title">Add Task', res_text)
        
        
    def test_insert_new_task(self):
        res = self.client.post('/insert_new_task', 
                               data=self.dummy_task, 
                               follow_redirects=True)
        dummy_task_description = mongo.db.tasks.find(
            {'description': self.dummy_task['description']})
        
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(dummy_task_description)


    def test_render_edit_task(self):
        dummy_task_id = mongo.db.tasks.insert_one(self.dummy_task).inserted_id
        res = self.client.get(f'/edit_task/{dummy_task_id}',
                              follow_redirects=True)
        res_text = res.get_data(as_text=True)     
        
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.dummy_task['description'], res_text)        


    def test_update_task(self):
        dummy_task_id = mongo.db.tasks.insert_one(self.dummy_task).inserted_id
        self.dummy_task['name'] = 'Testing Update Task'
        res = self.client.post(f'/update_task/{dummy_task_id}',
                               data=self.dummy_task,
                               follow_redirects=True)
        updated_dummy_task = mongo.db.tasks.find_one(
                                    {'_id': ObjectId(dummy_task_id)})
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.dummy_task['name'], 
                         updated_dummy_task.get('name'))
        

    def test_toggle_issue_sign_add(self):
        dummy_task_id = mongo.db.tasks.insert_one(self.dummy_task).inserted_id
        data = {'taskId': dummy_task_id}
        res = self.client.post('/toggle-issue-sign',
                               data=data,
                               follow_redirects=True)
        dummy_task_issue = mongo.db.tasks.find_one(
                                    {'_id': ObjectId(dummy_task_id)})

        self.assertEqual(res.status_code, 200)
        self.assertTrue(dummy_task_issue.get('issue'))        


    def test_toggle_issue_sign_remove(self):
        dummy_task_id = mongo.db.tasks.insert_one(self.dummy_task).inserted_id
        data = {'taskId': dummy_task_id}
        mongo.db.tasks.update_one({'_id': ObjectId(dummy_task_id)}, 
                                  {'$set': {'issue': True}})
        res = self.client.post('/toggle-issue-sign',
                               data=data,
                               follow_redirects=True)
        dummy_task_no_issue = mongo.db.tasks.find_one(
                                    {'_id': ObjectId(dummy_task_id)})
        
        self.assertEqual(res.status_code, 200)
        self.assertFalse(dummy_task_no_issue.get('issue')) 



if __name__ == '__main__':
    unittest.main()
