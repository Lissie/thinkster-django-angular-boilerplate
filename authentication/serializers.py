from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.models import Account

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    #We don't want to update the user's password unless they provide a new one
    #write_only, the actual password won't be shown in the AJAX response

    class Meta: #defines metadata the serializer requires to operate
        model = Account
        #we specify which attributes of the Account model should be serialized:
        fields = ('id', 'email', 'username', 'created_at', 'updated_at', 'first_name',
                  'tagline', 'password', 'confirm_password',)
        read_only_fields = ('created_at', 'updated_at',)

        #Turn JSON into a Python object. This is called deserialization and it is handled by:
        def create(self, validated_data): #Account.create()
            return Account.objects.create(**validated_data)

        def update(self, instance, validated_data): #instance is of type Account
            instance.username = validated_data.get('username', instance.username)
            instance.tagline = validated_data.get('tagline', instance.tagline)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password) #Store passwords in a secure way
                #This is a naive implementation of how to validate a password.
                #Not recommend for a real-world system
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)
            # When a user's password is updated, their session authentication hash must be
            # explicitly updated. If we don't do this here, the user will not be authenticated
            # on their next request and will have to log in again.

            return instance