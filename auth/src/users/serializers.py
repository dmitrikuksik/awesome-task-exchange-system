from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'public_id',
            'role',
            'role_display',
            'email',
            'first_name',
            'last_name',
        )