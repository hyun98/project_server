import json

from rest_framework.test import APITestCase, APIClient

from users.models import User, Profile
from reservations.models import Reservation


class ReservationTest(APITestCase):
    client = APIClient()
    headers = {}
    
    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'test1234@')
        self.user = user
        profile = Profile(user=user)
        profile.save()
        
    
    ## ==== Reservation TEST ====
    def test_reservation_date(self):
        reservation = Reservation(
            title="test", 
            floor=1,
            start_time="15:30",
            end_time="20:30",
            reserve_date="2021-09-20",
            booker=User.objects.get(id=1),
        )
        reservation.save()
        
        context = {
            'date': "2021-09-20",
        }
        
        response = self.client.post(
            '/api/v1/reservations/', 
            json.dumps(context), **self.headers, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
    
