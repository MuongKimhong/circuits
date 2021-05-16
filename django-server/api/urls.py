from django.urls import path

from .views import *


urlpatterns = [

    path('bcaou3gcauklbv3/register/', Register.as_view()),

    path('oq8va034o02cv26v2ckga/token-obtain/2lbcooo297cb19uz/', CustomTokenObtainPairView.as_view()),

    path('create-new-room/', CreateNewRoom.as_view()),

    path('check-password/', CheckIfRoomHasPassword.as_view()),
    
    path('join-room/', JoinRoom.as_view()),

    path('get-room-info/', GetRoomInfo.as_view()),

    path('get-room-members/', GetRoomMembers.as_view()),

    path('add-new-member/', AddRoomMember.as_view()),

    path('check-route-param/', CheckRoomRouteParam.as_view()),

    path('check-if-user-inside-room/', CheckIfUserInsideRoom.as_view()),

    path('remove-user-from-room/', RemoveUserFromRoom.as_view()),

    path('delete-room/', DeleteRoom.as_view()),

    path('room-count/', GetRoomOnline.as_view()),

    path('get-messages/', GetMessages.as_view()),

    path('send-message/', SendMessage.as_view()),
]