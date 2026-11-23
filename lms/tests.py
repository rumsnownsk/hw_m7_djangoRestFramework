import json
from django.utils import timezone

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from .models import Lesson, Course


class LessonTestCase(APITestCase):
    maxDiff = None

    def setUp(self):
        self.user = User.objects.create(email="testUser@test.com")
        self.course = Course.objects.create(title="Course for Lesson's test", description="desc course test")
        self.lesson = Lesson.objects.create(
            title="lesson for API_test",
            description="desc for API_test",
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """ тестирование получения одной сущности Урока """
        url = reverse("lms:lesson-detail", args=(self.lesson.pk,))

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('title'), self.lesson.title
        )

    def test_lesson_create(self):
        """ Тестирование создания Урока """
        url = reverse("lms:lesson-list")
        data = {
            "title": "lesson 2 for API_test",
            "description": "desc 2 for API_test",
            # "video_url": "https://youtu.be/dQw4w9WgXcQ",
            "course": self.course.pk,
            "owner": self.user.pk
        }
        response = self.client.post(url, data)
        # print(">>>>>:", response.json())
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        """ тестирование обновления сущности Урока """
        url = reverse("lms:lesson-detail", args=(self.lesson.pk,))

        upd_data = {
            "title": "UPDATE lesson 2 for API_test",
            "description": "UPDATE desc 2 for API_test",
        }
        response = self.client.patch(url, upd_data)

        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('title'), "UPDATE lesson 2 for API_test"
        )

    def test_lesson_delete(self):
        """ тестирование удаления сущности Урока """
        url = reverse("lms:lesson-detail", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("lms:lesson-list")
        response = self.client.get(url)

        response_json = response.json()

        for item in response_json["results"]:
            item.pop("created_at"); item.pop("updated_at")

        result = {
            "count": Lesson.objects.all().count(),
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "course_detail": {
                        "id": self.course.pk,
                        "title": "Course for Lesson's test",
                        "description": "desc course test"
                    },
                    "title": "lesson for API_test",
                    "video_url": None,
                    "preview": None,
                    "description": "desc for API_test",
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(response_json, result)


class CourseTestCase(APITestCase):
    maxDiff = None

    def setUp(self):
        self.user = User.objects.create(email="testUser@test.com")
        self.course = Course.objects.create(
            title="Course for Lesson's test", description="desc course test", owner=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """ тестирование получения одной сущности Курса """
        url = reverse("lms:courses-detail", args=(self.course.pk,))

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('title'), self.course.title
        )

    def test_course_create(self):
        """ Тестирование создания Курса """
        url = reverse("lms:courses-list")
        data = {
            "title": "course 2 for API_test",
            "description": "desc 2 for API_test",
        }
        response = self.client.post(url, data)
        # print(">>>>>:", response.json())
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        """ тестирование обновления сущности Курса """
        url = reverse("lms:courses-detail", args=(self.course.pk,))

        upd_data = {
            "title": "UPDATE course 2 for API_test",
            "description": "UPDATE course desc 2 for API_test",
        }
        response = self.client.patch(url, upd_data)

        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('title'), "UPDATE course 2 for API_test"
        )

    def test_course_delete(self):
        """ тестирование удаления сущности Курса """
        url = reverse("lms:courses-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        url = reverse("lms:courses-list")
        response = self.client.get(url)

        response_json = response.json()
        # print(json.dumps(response_json, indent=2))
        for item in response_json["results"]:
            item.pop("created_at"); item.pop("updated_at")

        result = {
            "count": Course.objects.count(),
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "lessons": [],
                    "count_lessons": self.course.lessons.count(),
                    "title": "Course for Lesson's test",
                    "preview": None,
                    "description": "desc course test",
                    "owner": self.user.pk
                }
            ]

        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(response_json, result)
