import datetime
from run import app, mongo
import unittest
import json

existing_collections = ['task_importance', 'tasks', 'task_category', 
                        'task_status']

time_stamp_obj = datetime.datetime.utcnow()
dummy_task = {'name': 'Testing Insert Task',
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
        if dummy_tasks:
            res = mongo.db.tasks.delete_one(task_description)

    
    def test_collections_exist(self):
        collections = mongo.db.list_collection_names()
        for collection in collections:
            self.assertIn(collection, existing_collections)
    
    
    def test_load_home_page(self):
        res = self.client.get('/')
        res_text = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('"brand-logo">Logo', res_text)
    
    
    def test_load_tasks_page(self):
        res = self.client.get('/tasks')
        res_text = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('"section-title">Tasks', res_text)
    
    
    def test_load_tasksdone_page(self):
        res = self.client.get('/tasks-done')
        res_text = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('"section-title">Completed Tasks', res_text)
    
    
    def test_insert_new_task(self):
        res = self.client.post('/insert_new_task', 
                               data=self.dummy_task, 
                               follow_redirects=True)
        dummy_task_description = mongo.db.tasks.find(
            {'description': self.dummy_task['description']})
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(dummy_task_description)



if __name__ == '__main__':
    unittest.main()
