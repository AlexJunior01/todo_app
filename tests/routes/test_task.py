
class TestPostTask:
    def test_post_valid_task(
            self,
            web_client,
            db_client,
            valid_task
    ):
        response = web_client.post('/task/', json=valid_task)
        body = response.json()
        task_id = body.pop('id')

        assert response.status_code == 200
        assert body == valid_task
        assert task_id is not None

    def test_post_invalid_task(
            self,
            web_client,
            db_client,
            invalid_task
    ):
        response = web_client.post('/task/', json=invalid_task)

        assert response.status_code == 422


class TestReadAllTask:
    def test_read_all_with_empty_database(
            self,
            web_client,
            db_client
    ):
        response = web_client.get('/task')
        body = response.json()

        assert len(body) == 0
        assert response.status_code == 200

    def test_read_all_with_tasks(
            self,
            web_client,
            db_client,
            valid_task
    ):
        web_client.post('/task/', json=valid_task)
        web_client.post('/task/', json=valid_task)

        response = web_client.get('/task')
        body = response.json()

        assert len(body) == 2
        assert response.status_code == 200


class TestReadTask:

    def test_read_valid_task(
            self,
            web_client,
            db_client,
            valid_task
    ):
        created_task = web_client.post('/task/', json=valid_task).json()

        response = web_client.get('/task/1')
        task = response.json()

        assert task == created_task
        assert response.status_code == 200

    def test_read_inexistent_task(
            self,
            web_client,
            db_client
    ):
        response = web_client.get('/task/1')
        body = response.json()

        assert response.status_code == 404
        assert body["message"] == "Task not found"


class TestDeleteTask:
    def test_delete_task_with_success(
            self,
            web_client,
            db_client,
            valid_task
    ):
        web_client.post('/task/', json=valid_task).json()

        response = web_client.delete('/task/1')
        body = response.json()

        recovered_task = web_client.get('/task/1')

        assert response.status_code == 200
        assert body["message"] == "Task deleted"
        assert recovered_task.status_code == 404

    def test_delete_inexistent_task(
            self,
            web_client,
            db_client
    ):
        response = web_client.delete('/task/1')
        body = response.json()

        assert response.status_code == 404
        assert body["message"] == "Task not found"


class TestUpdateTask:
    def test_update_task_with_success(
            self,
            web_client,
            db_client,
            valid_task
    ):
        web_client.post('/task/', json=valid_task).json()
        before_update_task = web_client.get('/task/1').json()

        response = web_client.patch('/task/1', json={'is_complete': True})
        body = response.json()
        print(body)

        after_update_task = web_client.get('/task/1').json()

        assert response.status_code == 200
        assert body["message"] == "Task updated"
        assert after_update_task
        assert before_update_task != after_update_task
        assert before_update_task["title"] == after_update_task["title"]

    def test_update_inexistent_task(
            self,
            web_client,
            db_client
    ):
        response = web_client.patch('/task/1', json={"is_complete": True})
        body = response.json()

        assert response.status_code == 404
        assert body["message"] == "Task not found"
