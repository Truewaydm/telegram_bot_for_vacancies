from rest_framework.serializers import (IntegerField, CharField, Serializer)
from post_in.notes.models import Note


class NoteSerializer(Serializer):
    id = IntegerField(read_only=True)
    title = CharField(required=True, max_length=255)
    text = CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('title', instance.text)
        instance.save()
        return instance
