from rest_framework.serializers import SerializerMethodField, ModelSerializer

from .models import Course, Lesson
from users.models import Payment


class LessonDetailSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'video_url')


class CourseSerializer(ModelSerializer):
    # lessons = SerializerMethodField()
    lessons = LessonDetailSerializer(many=True, read_only=True)
    count_lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lessons", "count_lessons"]  # подставьте свои поля

    def get_lessons(self, course):
        return Lesson.objects.filter(course=course)
        # return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    def get_count_lessons(self, obj):
        return obj.lessons.count()


class LessonSerializer(ModelSerializer):
    course = SerializerMethodField(read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_course(self, obj):
        if obj.course is None:
            return None

        course = obj.course
        return {
            'id':course.id,
            'title':course.title,
            'description':course.description
        }





