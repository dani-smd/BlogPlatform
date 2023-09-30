
from rest_framework import (permissions, status)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
# ---
from .serializer import ShowUserProfileSerializer, UpdateUserProfileParamsSerializer
# ---
from User_app.models import User


class ShowUserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        try:
            user_id = request.user.id
            qs_user = User.objects.get(id=user_id)
            user_profile = ShowUserProfileSerializer(qs_user)
            return Response({"data": user_profile.data, "message": "Profile retrieved successfully!", "status": 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data": None, "message": f"error: {str(e)}", "status": 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateUserProfileView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)
    serializer_class = UpdateUserProfileParamsSerializer

    def put(self, request) -> Response:
        try:
            user = request.user
            if request.POST.get('username', False):
                username = request.data['username']
                user.username = username
            if request.POST.get('email', False):
                email = request.data['email']
                user.email = email
            if request.POST.get('phone', False):
                phone = request.data['phone']
                user.phone_number = phone
            if request.POST.get('gender', False):
                gender = request.data['gender']
                user.gender = gender
            if request.FILES.get('image', False):
                image = request.FILES['image']
                user.user_image = image
            if not request.POST.get('username', False) and not request.POST.get('email', False) and \
                    not request.POST.get('phone', False) and not request.POST.get('gender', False) and \
                    not request.FILES.get('image', False):
                return Response({"data": None, "message": "Nothing Changed!", "status": 200},
                                status=status.HTTP_200_OK)
            else:
                user.save()
            # --- Response
            return Response({"data": None, "message": "Profile updated successfully!", "status": 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
