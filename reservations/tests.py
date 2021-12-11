import json

from rest_framework.test import APITestCase, APIClient

from users.models import User, Profile
from reservations.models import Reservation


class ReservationTest(APITestCase):
    client = APIClient()
    headers = {}
    
    def setUp(self):
        data = {
            'username': "admin",
            'email': "admin@admin.com",
            'password1': "admin",
            'last_name': "a",
            'first_name': "b",
            'gender': "M"
        }
        user = User.objects.create_user(data)
        self.user = user
        
    
    ## ==== Reservation TEST ====
    # def test_reservation_date(self):
    #     reservation = Reservation(
    #         title="test", 
    #         floor=1,
    #         start_time="15:30",
    #         end_time="20:30",
    #         reserve_date="2021-09-20",
    #         booker=self.user,
    #     )
    #     reservation.save()
        
    #     context = {
    #         'date': "2021-09-20",
    #     }
        
    #     response = self.client.get(
    #         '/api/v1/reservations/1', 
    #         json.dumps(context), **self.headers, content_type='application/json')
        
    #     self.assertEqual(response.status_code, 200)
    
