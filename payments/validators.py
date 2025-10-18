from rest_framework import serializers

def validate_positive_amount(amount):
    if amount is None or amount <= 0:
        raise serializers.ValidationError("Amount must be positive.")
    return amount
