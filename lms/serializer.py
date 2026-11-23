from rest_framework.fields import URLField
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField

from .models import Course, Lesson
from .validators import validate_forbidden_words, vld_video_url


class LessonSerializer(ModelSerializer):
    """ Вывод Уроков """
    course_detail = SerializerMethodField(read_only=True)
    title = CharField(validators=[validate_forbidden_words])
    video_url = URLField(validators=[vld_video_url], required=False)

    class Meta:
        model = Lesson
        # настройка для вывода полей при GET запросе
        fields = "__all__"
        extra_kwargs = {
            # "owner": {"read_only": True}
        }
        read_only_fields = ['created_at']
        # validators =

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
    """ Вывод Курсов """
    lessons = LessonShortSerializer(many=True, read_only=True)
    count_lessons = SerializerMethodField()
    title = CharField(validators=[validate_forbidden_words])


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