from rest_framework import serializers

from main.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'title', 'text')

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
