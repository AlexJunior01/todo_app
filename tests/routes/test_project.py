

class TestPostProject:
    def test_create_a_valid_project(self, web_client, db_client, valid_project):
        response = web_client.post("/project/", json=valid_project)
        project = response.json()

        assert response.status_code == 200
        assert project['id'] == 1

    def test_create_with_a_invalid_project(self, web_client, db_client, invalid_project):
        response = web_client.post("/project/", json=invalid_project)

        assert response.status_code == 422


class TestGetAllProjects:
    def test_read_all_projects_with_empty_db(self, web_client, db_client):
        response = web_client.get('/project/')
        body = response.json()

        assert response.status_code == 200
        assert body == []

    def test_read_all_projects(self, web_client, db_client, valid_project):
        web_client.post('/project/', json=valid_project)
        web_client.post('/project/', json=valid_project)

        response = web_client.get('/project/')
        body = response.json()

        assert response.status_code == 200
        assert len(body) == 2


class TestGetProject:
    def test_get_exitent_project(self, web_client, db_client, valid_project):
        created_project = web_client.post('/project/', json=valid_project).json()

        response = web_client.get('/project/1')
        body = response.json()

        assert response.status_code == 200
        assert body == created_project

    def test_get_inexitent_project(self, web_client, db_client):

        response = web_client.get('/project/1')
        body = response.json()

        assert response.status_code == 404
        assert body['message'] == 'Project not found.'


class TestPatchProject:
    def test_patch_project(self, web_client, db_client, valid_project):
        project_created = web_client.post('/project/', json=valid_project).json()

        response = web_client.patch('/project/1', json={'title': 'Test Updated'})
        project_updated = web_client.get('/project/1').json()

        assert response.status_code == 200
        assert project_updated['id'] == project_created['id']
        assert project_updated['title'] != project_created['title']

    def test_patch_inexistent_project(self, web_client, db_client):
        response = web_client.patch('/project/1', json={'title': 'Test Updated'})
        body = response.json()

        assert response.status_code == 404
        assert body['message'] == 'Project not found.'


class TestDeleteProject:
    def test_delete_existent_project(self, web_client, db_client, valid_project):
        project_created = web_client.post('/project/', json=valid_project).json()

        response = web_client.delete('/project/1')
        try_read_project_response = web_client.get('/project/1')

        assert response.status_code == 200
        assert try_read_project_response.status_code == 404

    def test_delete_existent_project_without_inform_delete_task_flag(
            self,
            web_client,
            db_client,
            valid_project,
            valid_task
    ):
        project_created = web_client.post('/project/', json=valid_project).json()
        task_created = web_client.post('/task/', json=valid_task)
        link_task_to_project_response = web_client.post('/project/1/task', json=[1])

        response = web_client.delete('/project/1')
        try_read_project_response = web_client.get('/project/1')
        task = web_client.get('/task/1').json()

        assert response.status_code == 200
        assert try_read_project_response.status_code == 404
        assert task['id'] == 1
        assert task['project_id'] is None

    def test_delete_existent_project_informing_delete_task_flag(
            self,
            web_client,
            db_client,
            valid_project,
            valid_task
    ):
        project_created = web_client.post('/project/', json=valid_project).json()
        task_created = web_client.post('/task/', json=valid_task)
        link_task_to_project_response = web_client.post('/project/1/task', json=[1])

        response = web_client.delete('/project/1', params={"delete_tasks": True})
        try_read_project_response = web_client.get('/project/1')
        try_read_task_response = web_client.get('/task/1')

        assert response.status_code == 200
        assert try_read_project_response.status_code == 404
        assert try_read_task_response.status_code == 404

    def test_delete_inexistent_project(self, web_client, db_client):

        response = web_client.delete('/project/1')
        body = response.json()

        assert response.status_code == 404
        assert body['message'] == 'Project not found.'


class TestAddTaskToProject:
    def test_try_to_add_task_to_inexistent_project(self, web_client, db_client):
        response = web_client.post('/project/99/task', json=[1, 2, 3])
        body = response.json()

        assert response.status_code == 404
        assert body['message'] == 'Project not found.'

    def test_try_to_add_inexistent_tasks_to_project(self, web_client, db_client, valid_project):
        project_created = web_client.post('/project/', json=valid_project)

        response = web_client.post('/project/1/task', json=[1, 2, 3])
        body = response.json()

        assert response.status_code == 400
        assert body['message'] == "Task_ids [1, 2, 3] do not exist."

    def test_adding_tasks_to_project(self, web_client, db_client, valid_project, valid_task):
        project_created = web_client.post('/project/', json=valid_project)
        task_created = web_client.post('/task/', json=valid_task)
        task_created = web_client.post('/task/', json=valid_task)

        response = web_client.post('/project/1/task', json=[1, 2])
        body = response.json()
        task_created = web_client.get('/task/1').json()

        assert response.status_code == 200
        assert body['message'] == "Tasks added to the project"
        assert task_created['project_id'] == 1

class TestRemoveTaskFromProject:
    def test_try_to_remove_task_from_inexistent_project(self, web_client, db_client):
        response = web_client.delete('/project/99/task', json=[1, 2, 3])
        body = response.json()

        assert response.status_code == 404
        assert body['message'] == 'Project not found.'

    def test_try_to_remove_inexistent_tasks_from_project(self, web_client, db_client, valid_project):
        project_created = web_client.post('/project/', json=valid_project)

        response = web_client.delete('/project/1/task', json=[1, 2, 3])
        body = response.json()

        assert response.status_code == 400
        assert body['message'] == "Task_ids [1, 2, 3] do not exist."

    def test_adding_tasks_to_project(self, web_client, db_client, valid_project, valid_task):
        project_created = web_client.post('/project/', json=valid_project)
        task_created = web_client.post('/task/', json=valid_task)
        task_created = web_client.post('/task/', json=valid_task)
        link_task_to_project_response = web_client.post('/project/1/task', json=[1, 2])

        response = web_client.delete('/project/1/task', json=[1, 2])
        body = response.json()
        task_created = web_client.get('/task/1').json()

        assert response.status_code == 200
        assert body['message'] == "Tasks removed from the project"
        assert task_created['project_id'] is None


class TestGetAllTaskOfProject:
    def test_read_tasks_from_inexistent_project(self, web_client, db_client):
        response = web_client.get('/project/99/task')
        body = response.json()

        assert response.status_code == 404
        assert body['message'] == 'Project not found.'

    def test_read_tasks_from_empty_project(self, web_client, db_client, valid_project):
        project_created = web_client.post('/project/', json=valid_project)

        response = web_client.get('/project/1/task')
        body = response.json()

        assert response.status_code == 200
        assert len(body) == 0

    def test_read_tasks_from_project_with_tasks(self, web_client, db_client, valid_project, valid_task):
        project_created = web_client.post('/project/', json=valid_project)
        task_created = web_client.post('/task/', json=valid_task)
        task_created = web_client.post('/task/', json=valid_task)
        link_task_to_project_response = web_client.post('/project/1/task', json=[1, 2])

        response = web_client.get('/project/1/task')
        body = response.json()

        assert response.status_code == 200
        assert len(body) == 2
