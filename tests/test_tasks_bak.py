import unittest
from ..app.tasks_bak import task_blue
from flask import Flask

app = Flask(__name__)
app.register_blueprint(task_blue)


class Testapp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()  # returns a new instance of the app in test_mode

    def test_1_get_list_tasks(self):
        response = self.client.get('/tasks')
        valid = {"result": [{"id": 1, "name": "name", "status": 0}]}
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, valid)

    def test_2_create_task(self):
        valid = {"result": {"id": 1, "name": "買早餐", "status": 0}}
        response = self.client.post('/task', json={"name": "買早餐"})
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.json, valid)
        response_int = self.client.post('/task', json={"name": 456})
        self.assertEqual(response_int.status_code, 400)

    def test_3_update_task(self):
        response = self.client.put('/task/1', json={"name": "買早餐", "status": 1, "id": 1})
        self.assertEqual(response.status_code, 200)

        valid = {"result": {"id": 1, "name": "買早餐", "status": 1}}
        self.assertDictEqual(response.json, valid)

        res_diff_id = self.client.put('/task/2', json={"name": "買早餐", "status": 1, "id": 1})
        self.assertEqual(res_diff_id.status_code, 400)

        res_diff_name = self.client.put('/task/1', json={"name": "買晚餐", "status": 1, "id": 1})
        self.assertEqual(res_diff_name.status_code, 400)

        res_key_err = self.client.put('/task/3', json={"name": "買早餐", "status": 1, "id": 3})
        self.assertEqual(res_key_err.status_code, 400)

        res_not_bool = self.client.put('/task/1', json={"name": "買早餐", "status": 3, "id": 1})
        self.assertEqual(res_not_bool.status_code, 400)

        res_loss = self.client.put('/task/1', json={"name": "買早餐", "status": 1})
        self.assertEqual(res_loss.status_code, 400)

    def test_4_delete_task(self):
        response = self.client.delete('/task/1')
        self.assertEqual(response.status_code, 200)

        res_none_num = self.client.delete('/task/2')
        self.assertEqual(res_none_num.status_code, 400)


if __name__ == '__main__':
    unittest.main()
