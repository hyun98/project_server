from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.db import transaction

from api.mixins import ApiAuthMixin, PublicApiMixin

from boards.serializers import PostDetailSerializer
from boards.models import Category, Post, PostFile
from users.models import User


class PostCreateApi(ApiAuthMixin, APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        cate_id 게시판에 새로운 글을 작성한다.
        title, content 필수
        
        첨부파일이 있는 경우
        {
            'upload_file': FILENAME
        }
        """
        cate_id = kwargs['cate_id']
        category = get_object_or_404(Category, pk=cate_id)
        
        title = request.data.get('title', '')
        content = request.data.get('content', '')
        
        if title == '' or content == '':
            return Response({
                "message": "title/content required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(username='admin')
        
        post = Post(
            creator=user, 
            category=category,
            title=title,
            content=content,
            thumbnail=request.data.get('thumbnail', ''),
        )
        
        post.save()
        
        files = request.FILES.getlist('upload_files')
        
        for file in files:
            postfile = PostFile(
                upload_files=file,
                filename=file.name,
                post=post
            )
            postfile.save()
        
        return Response({
            "message": "Post created success"
        }, status=status.HTTP_201_CREATED)


class PostManageApi(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        post_id에 맞는 글을 불러온다.
        쿠키를 사용한 조회수 체크
        유저당 10분에 한 번씩 해당 글의 조회수를 올릴 수 있다.
        """
        pk = kwargs['post_id']
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailSerializer(post, many=False)
        
        response = Response(serializer.data, status=status.HTTP_200_OK)
        
        expire_time = 600
        cookie_value = request.COOKIES.get('hitboard', '_')

        if f'_{pk}_' not in cookie_value:
            cookie_value += f'{pk}_'
            response.set_cookie(
                'hitboard', value=cookie_value, 
                max_age=expire_time, httponly=True)

            post.hits += 1
            post.save()
        
        return response
    
    def post(self, request, *args, **kwargs):
        """
        게시글 좋아요 기능.
        이미 좋아요를 누른 경우 취소
        """
        pk = kwargs['post_id']
        user = request.user
        if not pk:
            return Response({
                "message": "Select a post number"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        post = get_object_or_404(Post, pk=pk)
        
        if user.profile.favorite_post.filter(pk=pk).exists():
            user.profile.favorite_post.remove(post)
        else:
            user.profile.favorite_post.add(post)
            
        return Response({
            "message": "Post like/unlike success"
        }, status=status.HTTP_200_OK)
    
    
    def delete(self, request, *args, **kwargs):
        """
        글 삭제 기능.
        """
        post_id = kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        
        if request.user != post.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
    
        post.delete()
        
        return Response({
            "message": "Post delete success"
        }, status=status.HTTP_204_NO_CONTENT)
    
    
    def put(self, request, *args, **kwargs):
        """
        글 수정 기능.
        title, content, thumbnail 
        """
        post_id = kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        
        if request.user != post.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
        
        title = request.data.get("title")
        content = request.data.get("content")
        
        if title == '' or content == '':
            return Response({
                "message": "title required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
        post.title = title
        post.content = content
        post.thumbnail = request.data.get('thumbnail', '')
        
        post.save()
        
        return Response({
            "message": "Post update success"
        }, status=status.HTTP_201_CREATED)

