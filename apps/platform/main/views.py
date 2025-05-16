from rest_framework import views, permissions, status
from rest_framework.response import Response


# Main API view
# ----------------------------------------------------------------------------------------------------------------------
class MainAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    def get(self, request):
        context = {
            'page': 'Main page'
        }
        return Response(context, status=status.HTTP_200_OK)

