import os

from rest_framework import serializers

from vrc.settings import VALID_FILETYPES


def validate_res_field(value):
    if value % 2 != 0 or value < 20:
        raise serializers.ValidationError('Чётное число больше 20')
    return value


def validate_file_type(value):
    _, extension = os.path.splitext(str(value))
    if extension not in VALID_FILETYPES:
        raise serializers.ValidationError(
            f'Файл должен быть допустимого формата: {VALID_FILETYPES}'
        )
    return value
