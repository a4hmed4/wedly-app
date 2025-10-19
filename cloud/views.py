from typing import List

from django.conf import settings
from rest_framework.response import Response
from rest_framework import permissions, status, views

from accounts.permissions import IsAdmin
from .utils import firestore_list_collection


class FirestoreCollectionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request, collection: str):
        if not getattr(settings, 'FIRESTORE_ENABLED', False):
            return Response({"detail": "Firestore disabled"}, status=status.HTTP_400_BAD_REQUEST)

        page_size = int(request.query_params.get('page_size', settings.REST_FRAMEWORK.get('PAGE_SIZE', 10)))
        cursor = request.query_params.get('cursor')
        order_field = request.query_params.get('order_by')

        filters: List = []
        # Optional basic filter: ?where=field,==,value (repeatable)
        where_params = request.query_params.getlist('where')
        for w in where_params:
            parts = w.split(',', 2)
            if len(parts) == 3:
                filters.append((parts[0], parts[1], parts[2]))

        data = firestore_list_collection(
            collection=collection,
            order_field=order_field,
            page_size=page_size,
            cursor=cursor,
            filters=filters or None,
        )
        return Response(data)

