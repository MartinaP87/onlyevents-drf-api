from rest_framework import serializers
from .models import Profile, Preference


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    preferences = serializers.StringRelatedField(many=True)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'preferences',
            'name', 'content', 'image', 'is_owner'
        ]


class PreferenceSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')
    is_owner = serializers.SerializerMethodField()
    genre_name = serializers.SerializerMethodField()

    def get_genre_name(self, obj):
        return obj.genre.gen_name

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.profile.owner

    class Meta:
        model = Preference
        fields = [
            'id', 'profile', 'genre', 'genre_name', 'is_owner'
        ]
