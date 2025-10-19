import json
import os
from typing import Any, Dict, List, Optional, Tuple

from django.conf import settings

try:
    import firebase_admin
    from firebase_admin import credentials
    from google.cloud import firestore
except Exception:  # pragma: no cover
    firebase_admin = None
    credentials = None
    firestore = None


_firestore_client = None


def get_firestore_client():
    global _firestore_client
    if _firestore_client is not None:
        return _firestore_client

    if not getattr(settings, 'FIRESTORE_ENABLED', False):
        raise RuntimeError('Firestore is disabled. Set FIRESTORE_ENABLED=true in env.')

    project_id = getattr(settings, 'FIREBASE_PROJECT_ID', None)
    creds_json_or_path = getattr(settings, 'FIREBASE_CREDENTIALS_JSON', None)

    if not project_id or not creds_json_or_path:
        raise RuntimeError('Missing FIREBASE_PROJECT_ID or FIREBASE_CREDENTIALS_JSON in settings.')

    # Initialize firebase app if not already
    if firebase_admin and not firebase_admin._apps:
        if os.path.exists(creds_json_or_path):
            cred = credentials.Certificate(creds_json_or_path)
        else:
            cred = credentials.Certificate(json.loads(creds_json_or_path))
        firebase_admin.initialize_app(cred, {
            'projectId': project_id,
        })

    _firestore_client = firestore.Client(project=project_id)
    return _firestore_client


def firestore_list_collection(
    collection: str,
    order_field: Optional[str] = None,
    page_size: int = 10,
    cursor: Optional[str] = None,
    filters: Optional[List[Tuple[str, str, Any]]] = None,
) -> Dict[str, Any]:
    client = get_firestore_client()
    order_by_field = order_field or getattr(settings, 'FIRESTORE_DEFAULT_ORDER_FIELD', 'created_at')

    query = client.collection(collection).order_by(order_by_field)
    if filters:
        for field, op, value in filters:
            query = query.where(field, op, value)

    if cursor:
        # cursor should be a document id to start after
        last_doc = client.collection(collection).document(cursor).get()
        if last_doc.exists:
            query = query.start_after({order_by_field: last_doc.get(order_by_field)})

    docs = query.limit(page_size + 1).stream()
    docs_list = list(docs)
    has_more = len(docs_list) > page_size
    items = docs_list[:page_size]

    results = []
    next_cursor = None
    for d in items:
        data = d.to_dict() or {}
        data['id'] = d.id
        results.append(data)

    if has_more:
        next_cursor = items[-1].id

    return {
        'results': results,
        'next_cursor': next_cursor,
    }

