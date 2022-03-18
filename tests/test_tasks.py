import unittest
from ..app.tasks import task_blue
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
        self.assertDictEqual(response_int.json, {"result": {"name": ["Not a valid string."]}})

        response_none_type = self.client.post('/task', json={"name": "123", "id": 1})
        self.assertEqual(response_none_type.status_code, 400)
        self.assertDictEqual(response_none_type.json, {"result": {"id": ["Unknown field."]}})

    def test_3_update_task(self):
        res_str_status = self.client.put('/task/1', json={"name": "買早餐", "status": "1", "id": 1})
        res_str0_status = self.client.put('/task/1', json={"name": "買早餐", "status": "0", "id": 1})

        self.assertEqual(res_str_status.status_code, 400)
        self.assertDictEqual(res_str_status.json, {'result': {'status': ['Not a valid boolean.']}})
        self.assertDictEqual(res_str0_status.json, {'result': {'status': ['Not a valid boolean.']}})

        response = self.client.put('/task/1', json={"name": "買早餐", "status": 1, "id": 1})
        self.assertEqual(response.status_code, 200)

        valid = {"result": {"id": 1, "name": "買早餐", "status": 1}}
        self.assertDictEqual(response.json, valid)

        valid = {"result": {"id": 1, "name": "買早餐", "status": 1}}
        self.assertDictEqual(response.json, valid)

        res_diff_id = self.client.put('/task/2', json={"name": "買早餐", "status": 1, "id": 1})
        self.assertEqual(res_diff_id.status_code, 400)
        self.assertDictEqual(res_diff_id.json, {'result': 'KeyError'})

        res_diff_name = self.client.put('/task/1', json={"name": "買晚餐", "status": 1, "id": 1})
        self.assertEqual(res_diff_name.status_code, 400)
        self.assertDictEqual(res_diff_name.json, {'result': 'KeyError'})

        res_not_num = self.client.put('/task/3', json={"name": "買早餐", "status": 1, "id": 3})
        self.assertDictEqual(res_not_num.json, {'result': 'KeyError'})

        res_not_bool = self.client.put('/task/1', json={"name": "買早餐", "status": 3, "id": 1})
        self.assertEqual(res_not_bool.status_code, 400)
        self.assertDictEqual(res_not_bool.json, {"result": {"status": ["Not a valid boolean."]}})

        res_loss = self.client.put('/task/1', json={"name": "買早餐", "status": 1})
        self.assertEqual(res_loss.status_code, 400)
        self.assertDictEqual(res_loss.json, {"result": {"id": ["Missing data for required field."]}})

    def test_4_delete_task(self):
        response = self.client.delete('/task/1')
        self.assertEqual(response.status_code, 200)

        res_err_num = self.client.delete('/task/2')
        self.assertEqual(res_err_num.status_code, 400)
        self.assertDictEqual(res_err_num.json, {'result': 'KeyError'})

    if __name__ == '__main__':

        unittest.main()  # pragma: no cover
