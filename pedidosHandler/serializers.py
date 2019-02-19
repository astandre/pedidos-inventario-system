from rest_framework import serializers
from .models import *
import logging

#
# class ChannelInitSerializer(serializers.Serializer):
#     """
#     Serializer used to check data that comes from user, uses provided key to identify channel.
#     """
#     key = serializers.CharField(required=True, max_length=32)
#
#     def validate_key(self, key):
#         """
#         Function used to validate if key exists
#         :param key: key provided from system to use in chanel
#         :return: returns key if key exists otherwise raises a validation error.
#         """
#         try:
#             Channels.objects.get(key__iexact=key)
#         except Channels.DoesNotExist:
#             raise serializers.ValidationError("Wrong Access Key")
#         else:
#             return key
#
#     def update(self, instance, validated_data):
#         pass
#
#     def create(self, validated_data):
#         pass
