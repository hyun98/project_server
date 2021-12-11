import datetime
import json
from rest_framework.test import APITestCase, APIClient

from users.models import User, Profile
from survey.models import Survey, Question, SubQuestion, Applier, ApplyFile, Answer


class SurveyTest(APITestCase):
    client = APIClient()
    headers = {}
    
    def setUp(self):
        user = User.objects.create_superuser(username="admin", email="admin@admin.com", password="admin")
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
        jfile = open('testjson/testsurvey.json', 'r')
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
    

class SurveyApiTest(APITestCase):
    client = APIClient()
    headers = {}
    def setUp(self):
        user = User.objects.create_superuser(username="admin", email="admin@admin.com", password="admin")
        Survey(
            title = "test_survey",
            description = "test1\ntest2",
            start_date = "2021-10-01",
            due_date = "2021-12-01",
            created_date = datetime.datetime.now(),
            creator = user
        ).save()
    
    def test_survey_list(self):
        response = self.client.get(
            '/api/v1/survey/', 
            **self.headers, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
    
    