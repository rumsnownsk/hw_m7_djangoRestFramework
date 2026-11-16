from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    course_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"

    def get_course_detail(self, obj):
        return


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    count_lessons = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lessons", "count_lessons"]  # подставьте свои поля

    def get_count_lessons(self, inst):
        return inst.lessons.count()