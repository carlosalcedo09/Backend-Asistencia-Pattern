
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['full_name'] = user.get_full_name()
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Añade datos adicionales al response además de los tokens
        data['user'] = {
            'email': self.user.email,
            'full_name': self.user.get_full_name(), 
        }

        return data
