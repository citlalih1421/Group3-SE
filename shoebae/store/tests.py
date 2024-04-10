from django.test import TestCase

# Create your tests here.
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from store.models import Brand


#HERE I WILL TEST THE CLASS "BRAND" USING DIFFERENT INPUTS
class BrandTestCase(TestCase):

#THE SETUP METHOD IS CALLED TO CREATE TWO OBJECTS NAMED NIKE AND ADDIDAS 
    def setUp(self):
        self.nike_brand = Brand.objects.create(name="nike")
        self.addidas_brand = Brand.objects.create(name="addidas")


#CHECKING IF THE 'NAME' FIELD OF THE BRAND MODEL IS UNIQUE WITH THE INTENT OF FAILING
#IT CHECKS BY ATTEMPTING TO CREATE A BRAND NAMED NIKE AND THERE SHOULD ALREADY BE ONE IN THE DATABASE
    def test_brand_name_is_unique(self):
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name="nike")


#TESTING IF THE NAME FIELD HAS A MAX LENGTH OF 100 CHARACTERS BY ATTEMPTING TO MAKE A BRAND LONGER THAN 100
    def test_brand_name_max_length(self):
        long_name = "a" * 101
        brand = Brand(name=long_name)
        with self.assertRaises(ValidationError):
            brand.full_clean()


#TESTING TO SEE IF THE STRING METHOD OF THE BRAND MODEL IS WORKING CORRECTLY 
    def test_brand_str_method(self):
        self.assertEqual(str(self.nike_brand), "nike")


#CHECKS THE NUMBER OF BRAND OBJECTS IN THE DATABASE
    def test_brand_objects_count(self):
        self.assertEqual(Brand.objects.count(), 2)

    