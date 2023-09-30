from rest_framework import (permissions, status)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# ---
from Comment_app.serializer import CommentSerializer, CommentParamsSerializer, CommentUpdateParamsSerializer
from Comment_app.models import Comments
from Blog_app.models import Posts


class CommentViewSet(ModelViewSet):
    serializer_class = CommentParamsSerializer
    queryset = Comments.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'update':
            return CommentUpdateParamsSerializer
        if self.action == 'create':
            return CommentParamsSerializer
        return CommentUpdateParamsSerializer

    def list(self, request, *args, **kwargs) -> Response:
        try:
            post_id = self.kwargs['pk']
            post = Posts.objects.get(id=post_id)
            queryset = Comments.objects.filter(post=post, soft_delete=False)
            if queryset:
                return Response(
                    {'data': CommentSerializer(queryset, many=True).data,
                     'message': 'Comments listed successfully',
                     'status': 200}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'data': None, 'message': 'Comments not found', 'status': 404}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'data': None, 'message': f'"error": {str(e)}', 'status': 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs) -> Response:
        try:
            try:
                post_id = request.data['post']
                content = request.data['content']
            except Exception as e:
                return Response({'data': None, 'message': f"request body is incorrect, {str(e)}", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            if not content:
                return Response({'data': None, 'message': "Please enter comment content!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            if not post_id:
                return Response({'data': None, 'message': "Please enter post ID!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # ---
            qs_post = Posts.objects.get(id=post_id)
            if request.user.is_authenticated:
                user = request.user
                Comments.objects.create(post=qs_post, content=content, auther=user)
            else:
                Comments.objects.create(post=qs_post, content=content)
            # --- Response
            return Response({"data": None, "message": "Comment submitted successfully!", "status": 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data': None, 'message': f'"error": {str(e)}', 'status': 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs) -> Response:
        try:
            try:
                comment_id = request.data['comment_id']
                content = request.data['content']
            except Exception as e:
                return Response({'data': None, 'message': f"request body is incorrect, {str(e)}", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            if not content:
                return Response({'data': None, 'message': "Please enter comment content!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            if not comment_id:
                return Response({'data': None, 'message': "Please enter post ID!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # ---
            qs_comment = Comments.objects.get(id=comment_id)
            user = request.user
            if qs_comment.post.auther == user or qs_comment.auther == user:
                qs_comment.content = content
                qs_comment.save()
                # --- Response
                return Response({"data": None, "message": "Comment updated successfully!", "status": 200},
                                status=status.HTTP_200_OK)
            else:
                return Response({"data": None, "message": "You don't have permission!", "status": 400},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data': None, 'message': f'"error": {str(e)}', 'status': 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs) -> Response:
        try:
            try:
                comment_id = self.kwargs['pk']
            except Exception as e:
                return Response({'data': None, 'message': f"request body is incorrect, {str(e)}", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # ---
            if not comment_id:
                return Response({'data': None, 'message': "Please enter post ID!", 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            # ---
            qs_comment = Comments.objects.get(id=comment_id)
            user = request.user
            if qs_comment.post.auther == user or qs_comment.auther == user:
                qs_comment.soft_delete = True
                qs_comment.save()
                # --- Response
                return Response({"data": None, "message": "Comment deleted successfully!", "status": 200},
                                status=status.HTTP_200_OK)
            else:
                return Response({"data": None, "message": "You don't have permission!", "status": 400},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'data': None, 'message': f'"error": {str(e)}', 'status': 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)