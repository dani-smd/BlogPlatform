import re
import phonenumbers
from rest_framework import (permissions, status)
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
# ---
from User_app.models import User
from User_app.Authentication.auxiliary_functions import (generate_random_token, add_dict_to_redis, get_dict_from_redis)
from User_app.Authentication.auxiliary_functions import (delete_item_from_redis)
# ---
from .serializer import (RegisterUserParamsSerializer, LoginUserParamsSerializer, UserForgotPasswordParamsSerializer)
from .serializer import (CheckTokenParamsSerializer, UserResetPasswordParamsSerializer)


class UserRegistrationView(GenericAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = RegisterUserParamsSerializer

    def post(self, request):
        try:
            try:
                user_name = request.data['username']
                email = request.data['email']
                phone = request.data['phone']
                gender = request.data['gender']  # --- 'ML' as Male or 'FL' as Female
                password = request.data['password']
                image = request.FILES['image']
            except Exception as e:
                return Response({'data': None, 'message': f"request body is incorrect, {str(e)}", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # ---
            if not user_name:
                return Response({'data': None, 'message': "Please enter username!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            if not password:
                return Response({'data': None, 'message': "Please enter password!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            if email:
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                if not re.fullmatch(regex, email):
                    return Response({'data': None, 'message': "Please enter a valid email!", 'status': 400},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'data': None, 'message': "Please enter email!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # ---
            if phone:
                parse_number = phonenumbers.parse(phone, "IR")
                if not phonenumbers.is_valid_number_for_region(parse_number, "IR"):
                    return Response({'data': None, 'message': "Please enter a valid phone number!", 'status': 400},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'data': None, 'message': "Please enter phone number!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # --- Create User
            new_user = User.objects.create_user(username=user_name, email=email, password=password)
            new_user.phone_number = phone
            new_user.gender = gender
            new_user.user_image = image
            new_user.save()
            # --- get token
            refresh = RefreshToken.for_user(new_user)
            refresh_code = str(refresh)
            access_code = str(refresh.access_token)
            # --- response
            return Response({'data': {"access": access_code, "refresh": refresh_code},
                             'message': "Authorization token created successfully", 'status': 201},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data': None, 'message': f"error: {str(e)}", 'status': 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginUserView(GenericAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = LoginUserParamsSerializer

    def post(self, request):
        try:
            try:
                username = request.data['username']
                password = request.data['password']
            except Exception as e:
                return Response({'data': None, 'message': f"request body is incorrect, {str(e)}", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # ---
            if not username:
                return Response({'data': None, 'message': "Please enter username!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            if not password:
                return Response({'data': None, 'message': "Please enter password!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # ---
            qs_user = User.objects.filter(username=username)
            if not qs_user.exists():
                return Response({'data': None, 'message': "User does not exist!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # --- queryset user
            user = qs_user.first()
            if not user.check_password(password):
                return Response({'data': None, 'message': "Wrong Password!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # ---
            new_user = User.objects.get(username=username)
            # --- get token
            refresh = RefreshToken.for_user(new_user)
            refresh_code = str(refresh)
            access_code = str(refresh.access_token)
            # --- response
            return Response({'data': {"access": access_code, "refresh": refresh_code},
                             'message': "Login token created successfully", 'status': 201},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data': None, 'message': f"error: {str(e)}", 'status': 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsersForgotPasswordView(GenericAPIView):
    parser_classes = (FormParser,)
    serializer_class = UserForgotPasswordParamsSerializer

    def post(self, request):
        try:
            try:
                phone = request.data['phone']
            except Exception as e:
                return Response({'data': None, 'message': f"request body is incorrect, {str(e)}", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # ---
            if not phone:
                return Response({'data': None, 'message': "Please enter phone number!"},
                                status=status.HTTP_400_BAD_REQUEST)
            # --- validate phone
            user = User.objects.filter(phone_number=phone)
            if not user:
                return Response({'data': None, 'message': "User doesn't exist!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # --- generate token and send otp
            token = int(generate_random_token())
            # if send_message(phone, token, "eToken"):
            redis_data = {
                "token": token,
                "user_id": user.first().id
            }
            if add_dict_to_redis(f"{phone}_forgot_pass", redis_data, ex=1000):
                return Response(
                    {'data': {"Token": token, "expire_time": 120}, 'message': 'Token successfully sent!',
                     'status': 200}, status=status.HTTP_200_OK)
            else:
                return Response({'data': None, 'message': "Please try again!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # else:
            #     return Response({'message': "Please try again!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data': None, 'message': f"error: {str(e)}", 'status': 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # --- check otp and set password
    def put(self, request):
        try:
            try:
                phone = request.data['phone']
                token = request.data['token']
                new_password = request.data['new_password']
            except Exception as e:
                return Response({'data': None, 'message': f"request body is incorrect, {str(e)}", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # --- check null
            if not phone:
                return Response({'data': None, 'message': "Please enter phone!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            if not new_password:
                return Response({'data': None, 'message': "Please enter password!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            if not token:
                return Response({'data': None, 'message': "Please enter token!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # --- check token type
            elif not str(token).isnumeric():
                return Response({'data': None, 'message': "Please enter a valid token!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                # --- get redis data
                redis_data = get_dict_from_redis(f"{phone}_forgot_pass")
                if redis_data['status']:
                    data = redis_data['data']
                    # --- check token
                    redis_token = int(data['token'])
                    if redis_token != int(token):
                        return Response({'data': None, 'message': "Token isn't correct!", 'status': 400},
                                        status=status.HTTP_400_BAD_REQUEST)
                    # --- get user
                    user_id = data['user_id']
                    user = User.objects.get(id=user_id)
                    user.set_password(new_password)
                    user.save()
                    # --- Delete this record from redis
                    delete_item_from_redis(f"{phone}_forgot_pass")
                    # --- response
                    return Response({'data': None, 'message': "Password successfully changed!", 'status': 400},
                                    status=status.HTTP_200_OK)
                # --- something went wrong
                return Response({'data': None, 'message': "Token expired, try again!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data': None, 'message': f"error: {str(e)}", 'status': 400},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsersForgotPasswordCheckOTPView(GenericAPIView):
    parser_classes = (FormParser,)
    serializer_class = CheckTokenParamsSerializer

    # --- check otp is valid or not
    def post(self, request):
        try:
            # --- check params
            try:
                phone_number = request.data['phone']
                token = request.data['token']
            except Exception as e:
                return Response({'data': None, 'message': f"request body is incorrect, {str(e)}", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # --- check type
            if not str(token).isnumeric():
                return Response({'data': None, 'message': "Token must be integer", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # --- get redis data
            redis_data = get_dict_from_redis(f"{phone_number}_forgot_pass")
            if redis_data['status']:
                data = redis_data['data']
                # --- check token
                redis_token = int(data['token'])
                if redis_token != int(token):
                    return Response({'data': None, 'message': "Please enter a valid token!", 'status': 400},
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response({'data': None, 'message': "Token successfully verified!", 'status': 400},
                                status=status.HTTP_200_OK)
            return Response({'data': None, 'message': "Please try again!", 'status': 400},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data': None, 'message': f"error: {str(e)}", 'status': 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsersResetPasswordView(GenericAPIView):
    parser_classes = (FormParser,)
    serializer_class = UserResetPasswordParamsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # --- check body keys
            try:
                old_password = request.data['old_password']
                new_password = request.data['new_password']
            except Exception as e:
                return Response({'data': None, 'message': f"request body is incorrect, {str(e)}", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # ---
            if not old_password:
                return Response({'data': None, 'message': "Please enter your current password!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            if not new_password:
                return Response({'data': None, 'message': "Please enter your new password!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # --- check old pass
            if not request.user.check_password(old_password):
                return Response({'data': None, 'message': "The current password is incorrect!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # --- set new password
            request.user.set_password(new_password)
            request.user.save()
            # --- response
            return Response({'data': None, 'message': "Password successfully changed!", 'status': 400},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data': None, 'message': f"error: {str(e)}", 'status': 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
