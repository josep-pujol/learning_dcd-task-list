from run import app, test, mongo
import unittest


existing_collections = ['task_importance', 'tasks', 'task_category', 
                        'task_status']

class TestAppCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()
        

    def test_home(self):
        result = self.client.get('/')
        print(result)
        print('end test_home')


    def test_collections_exist(self):
        collections = mongo.db.list_collection_names()
        for collection in collections:
            self.assertIn(collection, existing_collections)
        

if __name__ == '__main__':
    unittest.main()
