from artikel.models import Artikel
from rest_framework import serializers

#~ class ArtikelSerializer(serializers.Serializer):
    #~ a_id    = serializers.IntegerField(read_only=True)
    #~ titel   = serializers.CharField(required=False, allow_blank=True, max_length=512)
    #~ text    = serializers.CharField()
    #~ tags    = serializers.CharField()
    #~ datum   = serializers.DateField()
    
    #~ def create(self, validated_data):
        #~ """
        #~ Create and return a new 'Artikel' instance, given the validated data.
        #~ """
        #~ return Artikel.objects.create(**validated_data)

    #~ def update(self, instance, validated_data):
        #~ """
        #~ Update and return an existing `Snippet` instance, given the validated data.
        #~ """
        #~ instance.titel  = validated_data.get('titel', instance.titel)
        #~ instance.text   = validated_data.get('text', instance.text)
        #~ instance.tags   = validated_data.get('tags', instance.tags)
        #~ instance.datum  = validated_data.get('datum', instance.datum)
        #~ instance.save()
        #~ return instance

class ArtikelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Artikel
        fields = ('a_id', 'titel', 'text', 'tags', 'datum')
