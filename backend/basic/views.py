from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class TestViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        auth = OIDCAuthenticationBackend()
        user = auth.get_userinfo(request.auth, None, None)
        return Response({'status': 'passt',
                         'user-email': request.user.email,
                         'user-username': request.user.username,
                         'auth': user}, status=status.HTTP_200_OK)
