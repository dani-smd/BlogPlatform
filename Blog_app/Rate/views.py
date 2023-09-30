
from rest_framework import (permissions, status)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Avg
# ---
from Blog_app.Rate.serializer import RateSerializer
from Blog_app.models import PostRate, Posts


class RateBlogView(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = RateSerializer

    def list(self, request, *args, **kwargs) -> Response:
        try:
            post_id = self.kwargs['pk']
            post = Posts.objects.get(id=post_id)
            queryset = PostRate.objects.filter(post=post)
            if queryset:
                result = queryset.aggregate(Avg('rate'))
                return Response({'data': result['rate__avg'], 'message': 'Rate calculated!', 'status': 200},
                                status=status.HTTP_200_OK)
            else:
                return Response({'data': None, 'message': 'Rate not found!', 'status': 404},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'data': None, 'message': f'"error": {str(e)}', 'status': 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs) -> Response:
        try:
            try:
                post_id = request.data['post']
                rate = request.data['rate']
            except Exception as e:
                return Response({'data': None, 'message': f"request body is incorrect, {str(e)}", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            print(type(rate))
            if not isinstance(int(rate), int) or rate > 5 or rate < 1:
                return Response({'data': None, 'message': "Rate must be integer and between 1-5!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            if not post_id:
                return Response({'data': None, 'message': "Please enter post ID!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # ---
            qs_post = Posts.objects.get(id=post_id)
            if request.user.is_authenticated:
                user = request.user
                PostRate.objects.create(post=qs_post, rate=rate, user=user)
            else:
                PostRate.objects.create(post=qs_post, rate=rate)
            # --- Response
            return Response({"data": None, "message": "Rate submitted successfully!", "status": 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data': None, 'message': f'"error": {str(e)}', 'status': 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
