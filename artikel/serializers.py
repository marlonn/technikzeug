from artikel.models import Artikel
from rest_framework import serializers
from django.contrib.auth.models import User

class ArtikelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta: 
        model = Artikel
        fields = ('a_id', 'titel', 'text', 'tags', 'datum', 'owner')
        
class UserSerializer(serializers.ModelSerializer):
    artikel =   serializers.PrimaryKeyRelatedField(
                    many=True,
                    queryset=Artikel.objects.all()
                )

    class Meta:
        model = User
        fields = ('id', 'username', 'artikel')
