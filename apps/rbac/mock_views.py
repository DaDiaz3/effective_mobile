from rest_framework.views import APIView
from rest_framework.response import Response

from apps.rbac.permissions import RBACPermission


class DocumentsMockView(APIView):
    permission_classes = [RBACPermission]
    rbac_element = "documents"

    def get(self, request):
        return Response([
            {"id": 1, "title": "Mock Document 1"},
            {"id": 2, "title": "Mock Document 2"},
        ])

    def post(self, request):
        return Response(
            {"id": 3, "title": request.data.get("title", "Untitled")},
            status=201
        )
