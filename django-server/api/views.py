import random 

from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from api.models import Room, Message


class Register(APIView):
    permission_classes = [ permissions.AllowAny ]

    def post(self, request):
        data = request.data
        
        if User.objects.filter(username=data['username']).exists():
            return Response({'username_taken': True}, status=400)

        user = User.objects.create_user(username=data['username'],
                                        password=data['password'])
        return Response({'success': True}, status=200)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'username': self.user.username})
        data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [ permissions.AllowAny ]


def room_object(room):
    object = {
        'id': room.id,
        'name': room.name,
        'ownerId': room.owner.id,
        'ownerName': room.owner.username,
        'token': room.token,
        'virtualId': room.virtualId,
        'slug': room.slug
    } 
    return object

class CreateNewRoom(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request):
        data = request.data
        user_id = data['user_id']

        if Room.objects.filter(name=data['name']).exists():
            return Response({ 'error': True }, status=400)

        room = Room.objects.create(owner_id=user_id, name=data['name'], password=data['password']) 
        return Response({ 'room': room_object(room) }, status=200)


class JoinRoom(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request):
        data = request.data
        room = Room.objects.get(virtualId=data['virtualId'])

        if room.password != data['password']:
            return Response({'errorPassword': True}, status=400)

        return Response({'room': room_object(room)}, status=200)
    

class CheckIfRoomHasPassword(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, request):
        if not Room.objects.filter(virtualId=request.GET['virtualId']).exists():
            return Response({ 'error': True }, status=400)

        room = Room.objects.get(virtualId=request.GET['virtualId'])
        response = {'no_password': True} if room.password == '' else {'no_password': False}
        return Response(response, status=200)


class GetRoomInfo(APIView):
    permission_classes = [ permissions.IsAuthenticated ]
    
    def get(self, request):
        room = Room.objects.get(id=request.GET['id'])
        return Response({'room': room_object(room)}, status=200)


class CheckRoomRouteParam(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, request):
        data = request.GET
        if not Room.objects.filter(id=data['id'], slug=data['slug'], token=data['token'], virtualId=data['virtualId'],
                                   owner__id=data['ownerId']):
            return Response({'error': True}, status=400)
        room = Room.objects.get(id=data['id'])
        return Response({'success': True, 'room': room_object(room)}, status=200)


class GetRoomMembers(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, request):
        room = Room.objects.get(id=request.GET['room_id'])

        colors = ['red', 'orange', 'purple', 'blue', 'green', 'cyan', 'pink darken-4', 'purple darken-4', 
                  'indigo darken-4', 'teal darken-4', 'blue-grey darken-4']

        members = [{
            'id': member.id,
            'name': member.username,
            'avatarColor': random.sample(colors, 1)[0],
            'avatarName' : member.username[0]
        } for member in room.members.all()]

        members.insert(0, {
            'id': room.owner.id,
            'name': room.owner.username,
            'avatarColor': 'blue',
            'avatarName': room.owner.username[0]
        })
        return Response({'members': members}, status=200)


class AddRoomMember(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request):
        print("added")
        room = Room.objects.get(id=request.data['room_id'])
        user = User.objects.get(id=request.data['user_id'])
        room.members.add(user)
        return Response({'success': True}, status=200)


class CheckIfUserInsideRoom(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, request):
        user = User.objects.get(id=request.GET['user_id'])
        room = Room.objects.get(id=request.GET['room_id'])

        res = {'in': True} if user in room.members.all() else {'in': False}
        return Response(res, status=200)


class RemoveUserFromRoom(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request):
        data = request.data
        user = User.objects.get(id=data['user_id'])
        room = Room.objects.get(id=data['room_id'])
        
        if user in room.members.all():
            room.members.remove(user)
        return Response({'success': True}, status=200)


class DeleteRoom(APIView):
    permission_classes = [ permissions.IsAuthenticated ]
    
    def post(self, request):
        room = Room.objects.get(id=request.data['room_id'])
        room.delete()
        return Response({ 'success': True }, status=200)


class GetRoomOnline(APIView):
    permission_classes = [ permissions.AllowAny ]

    def get(self, request):
        rooms = Room.objects.all().count()
        return Response({'rooms': rooms}, status=200)


def message_object(message):
    object = {
        'id'        : message.id,
        'senderName': message.sender.username,
        'senderId'  : message.sender.id,
        'date'      : message.date,
        'text'      : message.text
    }
    return object


class GetMessages(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, request):
        messages = Message.objects.filter(room__id=request.GET['room_id'])
        message_objects = [message_object(message) for message in messages]
        
        return Response({'messages': message_objects}, status=200)


class SendMessage(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request):
        data = request.data
        message = Message.objects.create(room_id=data['room_id'], sender_id=data['sender_id'], text=data['text'])
        return Response({'message': message_object(message)}, status=200)
