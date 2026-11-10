from django.shortcuts import render
from rest_framework import generics, viewsets

from lms.serializer import CourseSerializer, LessonSerializer

from .models import Course, Lesson

# Create your views here.


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """GET список уроков + POST создание"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курсов: list, retrieve, create, update, destroy"""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
