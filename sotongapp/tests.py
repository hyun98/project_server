from rest_framework.test import APITestCase, APIClient

from sotongapp.models import Organ

class DataSaveTest(APITestCase):
    client = APIClient()
    headers = {}
    
    def setUp(self):
        urlnames = ["project", 'bobel', 'ksu', 'vitamin', 'hyouth', 'volteer', 'deunsol']
        for name in urlnames:
            organ = Organ(name=name, urlname=name)
            organ.save()
        
    def test_sampledata(self):
        response = self.client.get(
            '/api/sotong/sampledata/0404', 
            **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
