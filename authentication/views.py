from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from authentication.models import Account
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        # If the method trying to be accessed is safe, we allow acces (not safe methods includes update and delete):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        # This method can be called by any user, since we want everyone to be able to register:
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        # It gets here when a non-safe method is trying to be accessed, then check is the user is logged and owner:
        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_404_BAD_REQUEST)