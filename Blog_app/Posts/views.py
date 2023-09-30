
from rest_framework import (permissions, status)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# ---
from Blog_app.Posts.serializer import PostParamsSerializer
from Blog_app.models import Posts


class CustomPagination(PageNumberPagination):
    page_size = 1
    # page_size_query_param = 'page_size'
    # max_page_size = 10

    def get_paginated_response(self, data):
        return Response({'data': {
            'links': {
                'next': self.page.next_page_number() if self.page.has_next() else None,
                'previous': self.page.previous_page_number() if self.page.has_previous() else None
            },
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', 1)),
            'page_size': self.page_size,
            'results': PostParamsSerializer(data, context={'request': self.request}, many=True).data
        }, 'message': "Post Paginated successfully!", 'status': 200}, status=status.HTTP_200_OK)


class PostViewSet(ModelViewSet):
    pagination_class = CustomPagination
    """
    In this class, we Manage our posts (List, create, retrieve, update, patch, destroy)
    """
    serializer_class = PostParamsSerializer
    queryset = Posts.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {'data': serializer.data, 'message': 'Post Listed successfully!',
             'status': 200}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs) -> Response:
        super().create(request, *args, **kwargs)
        return Response(
            {'data': None, 'message': 'Post created successfully!', 'status': 201}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs) -> Response:
        post_id = kwargs['pk']
        qs_post = Posts.objects.filter(id=post_id).first()
        if not qs_post:
            return Response({'data': None, 'message': 'Post not found!', 'status': 404},
                            status=status.HTTP_404_NOT_FOUND)
        super().list(request, *args, **kwargs)
        return Response(
            {'data': PostParamsSerializer(instance=self.get_object()).data, 'message': 'Post retrieved successfully!',
             'status': 200}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs) -> Response:
        # --- Check Auther
        user = request.user
        post_id = kwargs['pk']
        qs_post = Posts.objects.filter(id=post_id).first()
        if qs_post:
            if not qs_post.auther == user:
                return Response({'data': None, 'message': 'You are not Auther!', 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data': None, 'message': 'Post not found!', 'status': 404},
                            status=status.HTTP_404_NOT_FOUND)
        super().update(request, *args, **kwargs)
        return Response({'data': None, 'message': 'Post updated successfully!', 'status': 200},
                        status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs) -> Response:
        # --- Check Auther
        user = request.user
        post_id = kwargs['pk']
        qs_post = Posts.objects.filter(id=post_id).first()
        if qs_post:
            if not qs_post.auther == user:
                return Response({'data': None, 'message': 'You are not Auther!', 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data': None, 'message': 'Post not found!', 'status': 404},
                            status=status.HTTP_404_NOT_FOUND)
        super().update(request, *args, **kwargs)
        return Response({'data': None, 'message': 'Post updated successfully!', 'status': 200},
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs) -> Response:
        # --- Check Auther
        user = request.user
        post_id = kwargs['pk']
        qs_post = Posts.objects.filter(id=post_id).first()
        if qs_post:
            if not qs_post.auther == user:
                return Response({'data': None, 'message': 'You are not Auther!', 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data': None, 'message': 'Post not found!', 'status': 404},
                            status=status.HTTP_404_NOT_FOUND)
        super().destroy(request, *args, **kwargs)
        return Response({'data': None, 'message': 'Post deleted successfully!', 'status': 200},
                        status=status.HTTP_200_OK)
