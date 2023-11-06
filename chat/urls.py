
from .views import mark_as_seen


urlpatterns = [
    path("mark_messages/", mark_as_seen),
]