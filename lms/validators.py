import re

from rest_framework.serializers import ValidationError

forbidden_words = ["ставки", "крипта", "продам"]


YOUTUBE_PATTERN = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/[\w\-?=&/]+$"


def validate_forbidden_words(value):
    for word in forbidden_words:
        if word in value.lower():
            raise ValidationError(f"Слово <{value}> запрещено для использования")


def vld_video_url(value):
    if not re.match(YOUTUBE_PATTERN, value, flags=re.IGNORECASE):
        raise ValidationError("Ссылка должна вести на YouTube")
