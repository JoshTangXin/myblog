from rest_framework import serializers
from blog.models import Comment


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ("id","name","email","created","updated","body")