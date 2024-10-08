from rest_framework import serializers

from accounts.models import User
from .models import Article, Comment


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("author", "created_at", "updated_at")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("article")
        return ret


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("author",)


class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
