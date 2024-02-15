from rest_framework import serializers

def validate_res_field(value):
    if value % 2 != 0 or value < 20:
        raise serializers.ValidationError('Чётное число больше 20')
    return value
