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
    
    def test_create_survey(self):
        data = {
            "question": [
                {
                    "content": ["지원동기를 쓰세요"],
                    "description": ["궁금해요"],
                    "required": [True],
                    "order": [1],
                    "is_multichoice": [False],
                    "can_duplicate": [False],
                    "sub_question": []
                },
                {
                    "content": ["활동 기간을 선택해 주세요"],
                    "description": ["궁금해요"],
                    "required": [True],
                    "order": [2],
                    "is_multichoice": [True],
                    "can_duplicate": [False],
                    "sub_question": [
                        {
                            "sub_content": ["6개월"],
                            "can_select": [True]
                        },
                        {
                            "sub_content": ["1년 6개월"],
                            "can_select": [True]
                        },
                        {
                            "sub_content": ["기타"],
                            "can_select": [False]
                        }
                    ]
                },
                {
                    "content": ["하고싶은 주제"],
                    "description": ["궁금해요"],
                    "required": [True],
                    "order": [3],
                    "is_multichoice": [False],
                    "can_duplicate": [False],
                    "sub_question": []
                }
            ],
            "title": ["프로젝트 3기 모집 테스트 지원서"],
            "description": ["테스트입니다"],
            "start_date": ["2021-11-25"],
            "due_date": ["2021-11-30"]
        }
        
        response = self.client.post(
            '/api/v1/survey/', 
            json.dumps(data), **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 201, msg="Cannot create new survey")
    
    def test_read_survey_list(self):
        response = self.client.get(
            '/api/v1/survey/', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)


class SurveyApplyTest(APITestCase):
    client = APIClient()
    headers = {}
    
    def setUp(self):
        return super().setUp()
    
    def test_create_applier(self):
        # {
        #     "survey_id" : [1],
        #     "phone": ["123-123-123"],
        #     "name": ["hi"],
        #     "birth": ["1234123"],
        #     "gender": ["M"],
        #     "is_applied": [true],
        #     "answers": [
        #         {
        #             "question_id": [1],
        #             "answer": ["그냥그냥"]
        #         },
        #         {
        #             "question_id": [2],
        #             "answer": ["6개월", "2년"]
        #         },
        #         {
        #             "question_id": [3],
        #             "answer": ["없음"]
        #         }
        
        #     ]
        # }
        pass