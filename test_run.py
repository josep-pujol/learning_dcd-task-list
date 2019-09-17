from run import app, test, mongo
import unittest
import json

existing_collections = ['task_importance', 'tasks', 'task_category', 
                        'task_status']

class TestAppCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        
    
    def tearDown(self):
        pass
    
    
    def test_load_home_page(self):
        res = self.client.get('/')
        res_text = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('"brand-logo">Logo', res_text)


    def test_collections_exist(self):
        collections = mongo.db.list_collection_names()
        for collection in collections:
            self.assertIn(collection, existing_collections)
        

if __name__ == '__main__':
    unittest.main()
