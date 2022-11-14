

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

    def test_delete_inexistent_project(self, web_client, db_client):

        response = web_client.delete('/project/1')
        body = response.json()

        assert response.status_code == 404
        assert body['message'] == 'Project not found.'
