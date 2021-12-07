import json
from rest_framework.test import APITestCase, APIClient

from users.models import User, Profile
from survey.models import Survey, Question, SubQuestion, Applier, ApplyFile, Answer


class SurveyCreateTest(APITestCase):
    client = APIClient()
    headers = {}
    
    def setUp(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        self.user = user
        
        user = {
            "username": "admin",
            "password": "admin"
        }
        
        response = self.client.post('/api/v1/auth/login/', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200, msg="Login Failed")
        
        self.token = response.data['access_token']
        self.csrftoken = response.cookies.get('csrftoken').value
        
        self.assertNotEqual(self.token, '', msg="JWT Token not created")
        
        self.headers = {
            "HTTP_Authorization": "jwt " + self.token,
            "X-CSRFToken": self.csrftoken,
        }
    
    def test_survey(self):
        jfile = open('survey/testsurvey.json', 'r')
        data = json.load(jfile)
        jfile.close()
        
        response = self.client.post(
            '/api/v1/survey/', 
            json.dumps(data), **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 201, msg="Cannot create new survey")
        
        response = self.client.get(
            '/api/v1/survey/', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print(response.data)


class SurveyApplyTest(APITestCase):
    client = APIClient()
    headers = {}
    
    def setUp(self):
        return super().setUp()
    
    def test_create_applier(self):
        
        pass