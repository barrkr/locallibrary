from ninja import Schema, ModelSchema, FilterLookup, FilterSchema
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from chat.models import Room
from typing import Annotated
from django.db.models import Q
from chat.models import Message

class RoomIn(ModelSchema):
    class Meta:
        model = Room
        fields = ["name", "topic"]

class RoomOut(ModelSchema):
    class Meta:
        model = Room
        fields = ["id", "name", "topic", "created_at"]

class RoomFilter(FilterSchema):
    search: Annotated[str | None, FilterLookup("name__icontains")] = None
    topic: Annotated[str | None, FilterLookup("topic__icontains")] = None
    recent: bool | None = None
    def filter_recent(self, value: bool) -> Q:
        week_ago = timezone.now() - timedelta(days=7)
        return Q(created_at__gte=week_ago) if value else Q(created_at__lt=week_ago)

class Conflict(Schema):
    message: str
    existing_id: int

# chat/schemas.py
class MessageIn(ModelSchema):
    class Meta:
        model = Message
        fields = ["content"]


class MessageOut(ModelSchema):
    room: RoomOut

    class Meta:
        model = Message
        fields = ["id", "author", "content", "created_at"]
