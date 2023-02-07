from django.test import TestCase
from datetime import date, datetime

from .timetable_service import getDateAndTimeFromStr, getDateFromStr

# Create your tests here.
class DateServicesTests(TestCase):
    def setUp(self) -> None:
       self.dates = ['2022-12-13', '1970-01-01', '2011-13-122', '2011:13:12']
       self.datetimes = ['2022-12-13T13:24', '1970-01-01T01:56',
                         '2022-12-13T13:78', '1970-01-01K01:56']

    def test_get_date_from_str(self):
        self.assertEqual(getDateFromStr(self.dates[0]), date(2022, 12, 13)) 
        self.assertEqual(getDateFromStr(self.dates[1]), date(1970, 1, 1)) 
        with self.assertRaises(Exception):
            date_obj = getDateFromStr(self.dates[2])
            date_obj = getDateFromStr(self.dates[3])
    
    def test_get_datetime_from_str(self):
        self.assertEqual(getDateAndTimeFromStr(self.datetimes[0]), datetime(2022, 12, 13, 13, 24))
        self.assertEqual(getDateAndTimeFromStr(self.datetimes[1]), datetime(1970, 1, 1, 1, 56))
        with self.assertRaises(Exception):
            date_time = getDateAndTimeFromStr(self.datetimes[2])
            date_time = getDateAndTimeFromStr(self.datetimes[3])



    


        
        
