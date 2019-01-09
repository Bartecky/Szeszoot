#!/usr/bin/python3.7
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Player


@receiver(post_save, sender=Player)
def display_joined_player(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'game_{instance.game.id}',
            {
                'type': 'join_message',
                'message': instance.nickname
            }
        )