from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Course, Lesson


class LessonSerializer(ModelSerializer):
    course_detail = SerializerMethodField(read_only=True)

    class Meta:
        model = Lesson
        # настройка для вывода полей при GET запросе
        fields = "__all__"
        extra_kwargs = {
            # "owner": {"read_only": True}
        }
        read_only_fields = ['created_at']

    def get_course_detail(self, obj):
        if obj.course is None:
            return None

        course = obj.course
        return {
            "id": course.id,
            "title": course.title,
            "description": course.description,
        }


class LessonShortSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "title", "description", "video_url")

# class LessonShortSerializer(ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = ["id", "title", "description"]


class CourseSerializer(ModelSerializer):
    lessons = LessonShortSerializer(many=True, read_only=True)
    count_lessons = SerializerMethodField()

    class Meta:
        model = Course
        # fields = ["id", "title", "description", "lessons", "count_lessons"]
        fields = '__all__'
        read_only_fields = ['owner']

    def get_lessons(self, course):
        return Lesson.objects.filter(course=course)

    def get_count_lessons(self, obj):
        return obj.lessons.count()


class CourseShortSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description"]