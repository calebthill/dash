import unittest
import sys
import itertools

events = [
  { 'event': 'bill.split', 'user': 'Ray Green', 'city': 'Boston', 'time_of_day': 'morning', 'timestamp': 23981398 },
  { 'event': 'promo.used', 'user': 'Jon Wicks', 'city': 'New York', 'time_of_day': 'afternoon', 'amount': 10.0, 'timestamp': 93219323 },
  { 'event': 'promo.used', 'user': 'Robin Chou', 'city': 'New York', 'time_of_day': 'afternoon', 'amount': 15.0, 'timestamp': 28138233 },
  { 'event': 'bill.split', 'user': 'John Malcom', 'city': 'Chicago', 'time_of_day': 'evening', 'timestamp': 32189389 },
  { 'event': 'bill.split', 'user': 'Mark Wang', 'city': 'Boston', 'time_of_day': 'evening', 'timestamp': 43890121 }
]

key_names = ['event', 'city', 'time_of_day']

def validate_key_names(key_names, events):
    for key, event in itertools.product(key_names, events):
        k = event.get(key, None)
        if k is None:
            sys.exit("One of the key names is not valid")


def group_and_count(key_names, events):
  # Handle keys that are not valid. Not the most elegant solution, but works for this.
    validate_key_names(key_names, events)
    stats = {}
    
    for event in events:
        #link is the pointer to my current position in the stats dictionary
        link = stats
        # Here I'm creating keys that are met the first time when I iterate through events
        for l in key_names[0:-1]:
            k = event[l]
            # Here k is the actual value of a key
            if k not in link:
                link[k] = {}
            link = link[k]
        #the last key is the one I want to increment or create...
        if event[key_names[-1]] not in link:
            link[event[key_names[-1]]] = 1
        else:
            link[event[key_names[-1]]] = link[event[key_names[-1]]] + 1
    return stats

group_and_count(key_names, events)


# Im basically trying to create a multi-dimentional dictionary by saving my current position in link and 
# creating absent elements until I get to the last key name where I then increment. 


# TESTS
#-------------------------------------------------------------------------------------------------------

class MyTest(unittest.TestCase):
    
  def test_group_and_count_return_positive(self):
    key_names = ['event', 'city', 'time_of_day']
    return_value = {'promo.used': {'New York': {'afternoon': 2}}, 'bill.split': {'Boston': {'evening': 1, 'morning': 1}, 'Chicago': {'evening': 1}}}
    self.assertEqual(group_and_count(key_names, events), return_value)

  def test_group_and_count_return_length_positive(self):
    key_names = ['event', 'city', 'time_of_day']
    return_value = {'promo.used': {'New York': {'afternoon': 2}}, 'bill.split': {'Boston': {'evening': 1, 'morning': 1}, 'Chicago': {'evening': 1}}}
    self.assertEqual(len(group_and_count(key_names, events)), 2)

  def test_group_and_count_return_negative(self):
    key_names = ['event', 'city', 'time_of_day']
    return_value = {'wrong.value': {'New York': {'afternoon': 2}}, 'bill.split': {'Boston': {'evening': 1, 'morning': 1}, 'Chicago': {'evening': 1}}}
    self.assertNotEqual(group_and_count(key_names, events), return_value)

  def test_group_and_count_return_length_negative(self):
    key_names = ['event', 'city', 'time_of_day']
    return_value = {'promo.used': {'New York': {'afternoon': 2}}, 'bill.split': {'Boston': {'evening': 1, 'morning': 1}, 'Chicago': {'evening': 1}}}
    self.assertNotEqual(len(group_and_count(key_names, events)), 4)


if __name__ == '__main__':
  unittest.main()
  
