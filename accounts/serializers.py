from rest_framework import serializers
from .models import *

class UserSignupSerializer(serializers.ModelSerializer):
    ''' 
    User Signup serializer used to validate user information
    and insert into database. 
    '''
    password2=serializers.CharField(
        style={'input_type':'password'},
        write_only=True
    )
    class Meta:
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password does\'t match!')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserSigninSerializer(serializers.ModelSerializer):
    email=serializers.CharField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name','tc']
