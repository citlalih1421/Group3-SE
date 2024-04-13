from django.test import TestCase

# Create your tests here.

 from main import Add

def TestAdd():
    assert Add(2,3) == 5
    assert Add(5,5) == 10
    print("Works")

if __name__ == '__main__':
    TestAdd()
