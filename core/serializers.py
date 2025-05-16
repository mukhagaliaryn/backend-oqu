# Base serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


# User
# ----------------------------------------------------------------------------------------------------------------------
class UserSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'full_name', )


# UserAccount
# ----------------------------------------------------------------------------------------------------------------------
class UserAccountSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'avatar', 'google_avatar', 'account', )