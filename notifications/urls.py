from django.urls import path
from .views import NotificationListView, NotificationMarkReadView, NotificationDeleteView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('mark-read/<int:pk>/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('delete/<int:pk>/', NotificationDeleteView.as_view(), name='notification-delete'),
]
