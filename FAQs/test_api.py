import json

from rest_framework.test import APITestCase, APIClient

from FAQs.models import Question, Answer

class FAQslistAPITest(APITestCase):
    client = APIClient()
    headers = {}
    
    def setUp(self):
        Q1 = Question(
            order=1,
            question="q1"
        )
        Q1.save()
        
        A1 = Answer(
            answer="a1",
            question=Q1
        )
        A1.save()
    
    def test_FAQList(self):
        response = self.client.get(
            '/api/v1/faqs/', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        fd = {"faqs": [{"question":"q1", "answer":"a1"}]}
        self.assertEqual(data, fd)
    