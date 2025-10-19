from django.urls import path
from .views import FirestoreCollectionView


urlpatterns = [
    path('fs/<str:collection>/', FirestoreCollectionView.as_view(), name='cloud-firestore-collection'),
]

