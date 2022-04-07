from rest_framework import serializers
from .models import Route
"""
Jun Zhou
2022/4/6
NO right truly reserved
"""
class updateRouteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Route
        fields = ('id','code','geo_codes','addrs')

class createRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('code','geo_codes','addrs')

class routeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Route
        fields = ('id','code','geo_codes','addrs','total_dist','image_url','total_time')
