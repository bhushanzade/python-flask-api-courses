import unittest
import requests
import datetime

class ApiTestGetAllCourses(unittest.TestCase):
    url = 'http://localhost:5000'
    course_url = '{}/course'.format(url)

    def test_1(self):
        r = requests.get(ApiTestGetAllCourses.course_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

    def test_2(self):
        # Parameter with page sizes only
        params = {
            'page-size' : 20
        }
        r = requests.get(ApiTestGetAllCourses.course_url,params=params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

    def test_3(self):
        # Parameter with page sizes only
        params = {
            'page-size' : 20,
            'page-number' : 8
        }
        r = requests.get(ApiTestGetAllCourses.course_url,params=params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

    def test_4(self):
        # Worng page number
        params = {
            'page-size' : 20,
            'page-number' : 15
        }

        error_obj = {"message": "Invalid page no."}

        r = requests.get(ApiTestGetAllCourses.course_url,params=params)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(len(r.json()), 1)
        self.assertDictEqual(r.json(),error_obj)

    def test_5(self):
        # Get title filter results
        params = {
            'page-size' : 20,
            'title-words' : 'Cracking the Secrets, PowerPoint'
        }

        r = requests.get(ApiTestGetAllCourses.course_url,params=params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)



class ApiTestGetCourseById(unittest.TestCase):
    url = 'http://localhost:5000'
    course_url = '{}/course'.format(url)

    def test_1(self):
        # Test successfully get course
        get_url = '{}/150'.format(ApiTestGetCourseById.course_url)
        obj = {
            "data": {
                "date_created": "2019-09-04 02:16:01",
                "date_updated": "2020-09-10 19:17:38",
                "description": "Mockplus is tool for designing and rototyping user interfaces..",
                "discount_price": 3,
                "id": 150,
                "image_path": "",
                "on_discount": False,
                "price": 30,
                "title": "Mockplus! Mockplus!! Mockplus!!!"
            }
        }
        r = requests.get(get_url)
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(),obj)
    
    def test_2(self):
        get_url = '{}/309'.format(ApiTestGetCourseById.course_url)
        obj = {"message": "Course 309 does not exist"}
        r = requests.get(get_url)
        self.assertEqual(r.status_code, 404)
        self.assertDictEqual(r.json(),obj)
        

class ApiTestCreateCourse(unittest.TestCase):
    url = 'http://localhost:5000'
    course_url = '{}/course'.format(url)

    def test_1(self):
        obj = {
            "description": "Brand new course 1 wu ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab dhad habdkba kdbask bascbxncbmxnc m bmxbcnmzcb znmbc abc ahbc zbcxkbcz",
            "discount_price": 5,
            "title": "Brand new course 1 wu ahsdhas ",
            "price": 25,
            "image_path": "images/some/path/foo.jpg",
            "on_discount": False
        }
        
        r = requests.post(ApiTestCreateCourse.course_url, json=obj)

        createdobj = {
            "data": {
                "date_created": datetime.datetime.now().strftime('%Y-%m-%d %X'),
                "date_updated": datetime.datetime.now().strftime('%Y-%m-%d %X'),
                "description": "Brand new course 1 wu ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab dhad habdkba kdbask bascbxncbmxnc m bmxbcnmzcb znmbc abc ahbc zbcxkbcz",
                "discount_price": 5,
                "id": 201,
                "image_path": "images/some/path/foo.jpg",
                "on_discount": False,
                "price": 25,
                "title": "Brand new course 1 wu ahsdhas "
            }
        }

        self.assertEqual(r.status_code, 201)
        self.assertDictEqual(r.json(),createdobj)

    def test_2(self):
        # Title already exist Test Case
        obj = {
            "description": "Brand new course 1 wu ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab dhad habdkba kdbask bascbxncbmxnc m bmxbcnmzcb znmbc abc ahbc zbcxkbcz",
            "discount_price": 5,
            "title": "Brand new course 1 wu ahsdhas ",
            "price": 25,
            "image_path": "images/some/path/foo.jpg",
            "on_discount": False
        }
        errorobj = [{'error_message': 'title is already present.', 'feild_name': 'title'}]
        r = requests.post(ApiTestCreateCourse.course_url, json=obj)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(),errorobj)

    def test_3(self):
        # Title not exist Test Case
        obj = {
            "description": "Brand new course 1 wu ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab dhad habdkba kdbask bascbxncbmxnc m bmxbcnmzcb znmbc abc ahbc zbcxkbcz",
            "discount_price": 5,
            "price": 25,
            "image_path": "images/some/path/foo.jpg",
            "on_discount": False
        }

        errorobj = [
            {
                "error_message": "title is invalid.",
                "feild_name": "title"
            }
        ]

        r = requests.post(ApiTestCreateCourse.course_url, json=obj)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(),errorobj)

    def test_4(self):
        # Title and price not exist Test Case
        obj = {
            "description": "Brand new course 1 wu ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab dhad habdkba kdbask bascbxncbmxnc m bmxbcnmzcb znmbc abc ahbc zbcxkbcz",
            "discount_price": 5,
            "image_path": "images/some/path/foo.jpg",
            "on_discount": False
        }

        errorobj = [
            {
                "error_message": "price is invalid.",
                "feild_name": "price"
            },
            {
                "error_message": "title is invalid.",
                "feild_name": "title"
            }
        ]

        r = requests.post(ApiTestCreateCourse.course_url, json=obj)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(),errorobj)

    def test_5(self):
        # Description max length and title max length Test
        obj = {
            "description": "Brand new course 1 wu ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab dhad habdkba kdbask bascbxncbmxnc m bmxbcnmzcb znmbc abc ahbc zbcxkbcz Brand new course 1 wu ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab dhad habdkba kdbask bascbxncbmxnc m bmxbcnmzcb znmbc abc ahbc zbcxkbcz",
            "discount_price": 5,
            "title": "Brand new course 1 wu ahsdhas 34 new course 1 wu ahsdhas 34 ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab",
            "price": 25,
            "image_path": "images/some/path/foo.jpg",
            "on_discount": False
        }

        errorobj = [
            {
                "error_message": "description maximum length is 255.",
                "feild_name": "description"
            },
            {
                "error_message": "title maximum length is 100.",
                "feild_name": "title"
            }
        ]

        r = requests.post(ApiTestCreateCourse.course_url, json=obj)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(),errorobj)

    def test_6(self):
        # Title min length Test
        obj = {
            "description": "Brand new course.",
            "discount_price": 5,
            "title": "abc",
            "price": 25,
            "image_path": "images/some/path/foo.jpg",
            "on_discount": False
        }

        errorobj = [
            {
                "error_message": "title minimum length is 5.",
                "feild_name": "title"
            }
        ]

        r = requests.post(ApiTestCreateCourse.course_url, json=obj)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(),errorobj)


class ApiTestUpdateCourse(unittest.TestCase):
    url = 'http://localhost:5000'
    course_url = '{}/course'.format(url)

    def test_1(self):
        # test case for update successfully
        update_url = '{}/166'.format(ApiTestUpdateCourse.course_url)

        obj = {
            "description": "This is a brand new course",
            "discount_price": 5,
            "title": "Brand new course",
            "price": 25,
            "image_path": "images/some/path/foo.jpg",
            "on_discount": False
        }

        r = requests.put(update_url, json=obj)

        updated_obj = {
            "data": {
                "date_updated": datetime.datetime.now().strftime('%Y-%m-%d %X'),
                "description": "This is a brand new course",
                "discount_price": 5,
                "id": 166,
                "image_path": "images/some/path/foo.jpg",
                "on_discount": False,
                "price": 25,
                "title": "Brand new course"
            }
        }

        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(),updated_obj)

    def test_2(self):
        # test case for id not present
        update_url = '{}/207'.format(ApiTestUpdateCourse.course_url)
        obj = {
            "description": "Brand new course 1 wu ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab dhad habdkba kdbask bascbxncbmxnc m bmxbcnmzcb znmbc abc ahbc zbcxkbcz",
            "discount_price": 5,
            "title": "Brand new course 1 wu ahsdhas ",
            "price": 25,
            "image_path": "images/some/path/foo.jpg",
            "on_discount": False
        }

        error_obj = {"message": "The id does match the payload"}

        r = requests.put(update_url, json=obj)
        self.assertEqual(r.status_code, 400)
        self.assertDictEqual(r.json(),error_obj)

    def test_3(self):
        # Title not exist Test Case
        update_url = '{}/166'.format(ApiTestUpdateCourse.course_url)
        obj = {
            "description": "Brand new course 1 wu ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab dhad habdkba kdbask bascbxncbmxnc m bmxbcnmzcb znmbc abc ahbc zbcxkbcz",
            "discount_price": 5,
            "price": 25,
            "image_path": "images/some/path/foo.jpg",
            "on_discount": False
        }

        errorobj = [
            {
                "error_message": "title is invalid.",
                "feild_name": "title"
            }
        ]

        r = requests.put(update_url, json=obj)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(),errorobj)

    def test_4(self):
        # Title and price not exist Test Case
        update_url = '{}/166'.format(ApiTestUpdateCourse.course_url)
        obj = {
            "description": "Brand new course 1 wu ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab dhad habdkba kdbask bascbxncbmxnc m bmxbcnmzcb znmbc abc ahbc zbcxkbcz",
            "discount_price": 5,
            "image_path": "images/some/path/foo.jpg",
            "on_discount": False
        }

        errorobj = [
            {
                "error_message": "price is invalid.",
                "feild_name": "price"
            },
            {
                "error_message": "title is invalid.",
                "feild_name": "title"
            }
        ]

        r = requests.put(update_url, json=obj)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(),errorobj)

    def test_5(self):
        # Description max length and title max length Test
        update_url = '{}/166'.format(ApiTestUpdateCourse.course_url)
        obj = {
            "description": "Brand new course 1 wu ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab dhad habdkba kdbask bascbxncbmxnc m bmxbcnmzcb znmbc abc ahbc zbcxkbcz Brand new course 1 wu ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab dhad habdkba kdbask bascbxncbmxnc m bmxbcnmzcb znmbc abc ahbc zbcxkbcz",
            "discount_price": 5,
            "title": "Brand new course 1 wu ahsdhas 34 new course 1 wu ahsdhas 34 ahsdhas kdjhakjdh akshdjahs jkahd jahsdjha ahsd jab",
            "price": 25,
            "image_path": "images/some/path/foo.jpg",
            "on_discount": False
        }

        errorobj = [
            {
                "error_message": "description maximum length is 255.",
                "feild_name": "description"
            },
            {
                "error_message": "title maximum length is 100.",
                "feild_name": "title"
            }
        ]

        r = requests.put(update_url, json=obj)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(),errorobj)

    def test_6(self):
        # Title min length Test
        update_url = '{}/166'.format(ApiTestUpdateCourse.course_url)
        obj = {
            "description": "Brand new course.",
            "discount_price": 5,
            "title": "abc",
            "price": 25,
            "image_path": "images/some/path/foo.jpg",
            "on_discount": False
        }

        errorobj = [
            {
                "error_message": "title minimum length is 5.",
                "feild_name": "title"
            }
        ]

        r = requests.put(update_url, json=obj)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(),errorobj)


class ApiTestDeleteCourse(unittest.TestCase):
    url = 'http://localhost:5000'
    course_url = '{}/course'.format(url)

    def test_1(self):
        # Delete Successfull Test
        delete_url = '{}/130'.format(ApiTestDeleteCourse.course_url)
        delete_obj = {"message": "The specified course was deleted"}
        r = requests.delete(delete_url)
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(),delete_obj)

    def test_2(self):
        # Id not found this test will success if test 1 is completed
        delete_url = '{}/130'.format(ApiTestDeleteCourse.course_url)
        delete_obj = {"message": "Course 130 does not exist"}
        r = requests.delete(delete_url)
        self.assertEqual(r.status_code, 404)
        self.assertDictEqual(r.json(),delete_obj)

    def test_3(self):
        # Unknown Id
        delete_url = '{}/504'.format(ApiTestDeleteCourse.course_url)
        delete_obj = {"message": "Course 504 does not exist"}
        r = requests.delete(delete_url)
        self.assertEqual(r.status_code, 404)
        self.assertDictEqual(r.json(),delete_obj)
        

if __name__ == '__main__':
    unittest.main()