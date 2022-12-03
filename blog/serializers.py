from dataclasses import fields
from .models import Blog, Comment, Like
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    liked_by_me = serializers.SerializerMethodField()
    writter_email = serializers.EmailField(source='writter.email')

    class Meta:
        model = Comment
        fields=['id', 'text', 'writter_email', 'reply', 'likes', 'liked_by_me']

    def get_reply(self, instance):
        replies = Comment.objects.filter(root_node_type='Comment', root_node_id=instance.id)
        return CommentSerializer(replies, many=True).data

    def get_likes(self, instance):
        return Like.objects.filter(root_node_type='Comment', root_node_id=instance.id).count()

    def get_liked_by_me(self, instance):
        user_id = self.context.get('user_id', 0)
        return Like.objects.filter(root_node_type='Comment', root_node_id=instance.id, owner_id=user_id).exists()

class BlogSerilaizer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    liked_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields=['id', 'text', 'title', 'created', 'comment', 'likes', 'liked_by_me']

    def get_comment(self, instance):
        replies = Comment.objects.filter(root_node_type='Blog', root_node_id=instance.id)
        return CommentSerializer(replies, many=True).data

    def get_likes(self, instance):
        return Like.objects.filter(root_node_type='Blog', root_node_id=instance.id).count()

    def get_liked_by_me(self, instance):
        user_id = self.context.get('user_id', 0)
        return Like.objects.filter(root_node_type='Blog', root_node_id=instance.id, owner_id=user_id).exists()