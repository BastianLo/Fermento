from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


@api_view(['POST'])
def api_login(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)
