from rest_framework import serializers
import re


class CustomUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)
    
    
    
    def validate_phone_number(self, phone_number):
        
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise serializers.ValidationError("Phone number must be a 10-digit number.")
        return phone_number

    def validate_password(self, password):
        
        password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!])(?=\S+$).{8,}$'
        if not re.match(password_pattern, password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter, one lowercase letter, one digit, one special character, and at least 8 characters.")
        return password