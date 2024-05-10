# from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import  api_view
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from posts.models import Post
from .models import Like, Comment
from .serializers import CommentSerializer
from .permissions import IsOwnerOrReadOnly

@api_view(['POST'])
def toggle_like(request, id):
    user = request.user
    if not user.is_authenticated:
        return Response(status=401)
    post = get_object_or_404(Post, id=id)
    if Like.objects.filter(user=user, post=post).exists():
        Like.objects.filter(user=user, post=post).delete()        
    else:
        Like.objects.create(user=user, post=post)
    return Response(201)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[AllowAny]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update','partial_update','destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in self.permission_classes]