<template>
    <div class="mx-5">
        <v-row>

            <div hidden id="audio-grid"></div>

            <v-col cols=12 class="col-lg-3 col-md-3 col-sm-3 pl-5 pr-0" id="users-card" style="height: 90vh">
                <h2 class="white--text pt-5" align="center">Room id: {{ room.virtualId }}</h2>
                <h3 class="white--text pb-5" align="center">Room name: {{ room.name }}</h3>
                <v-card flat class="py-5 grey darken-2">
                    <!-- owner -->
                    <v-row class="py-3" v-for="member in roomMembers" :key="member.id">
                        <v-avatar :color="member.avatarColor" size="36">
                            <span class="white--text">{{ member.avatarName }}</span>
                        </v-avatar>
                        <span class="white--text ml-2 mt-2">{{ member.name }}</span>
                    </v-row>
                </v-card>
                <v-footer class="grey darken-4">
                    <v-btn class="col-12 text-capitalize red white--text"
                           v-if="$store.state.user.id != room.ownerId"
                           @click="leaveCall()">
                        Leave
                    </v-btn>
                    <v-btn class="col-12 text-capitalize red white--text"
                           v-else @click="endCall()">
                        End call
                    </v-btn>
                </v-footer>
            </v-col>   

            <v-col cols=12 class="col-lg-9 col-md-9 col-sm-9 pr-5 py-0"  id="message-col" style="height: 90vh">
                <!-- messages -->
                <div class="mt-5" style="height: 90%" id="scroll-content">
                    <div class="ml-5 mt-5 mb-5 pb-4" v-for="message in messages" :key="message.id">
                        <h6 class="white--text" style="margin-left: 30px">{{ message.senderName }}</h6>
                        <v-row class="mt-1">
                            <v-avatar :color="message.avatarColor" size="36">
                                <span class="white--text">{{ message.avatarName }}</span>
                            </v-avatar>
                            
                            <v-chip class="mt-1 ml-1">{{ message.text }}</v-chip>

                        </v-row>
                    </div>
                </div>

                <!-- send message -->

                <div class="px-5">
                    <v-row>
                        <v-text-field label="Message" color="#FFFFFF" dark v-model="message"></v-text-field>
                        <v-btn rounded class="text-capitalize mt-3" @click="sendMessage()">Send</v-btn>
                    </v-row>   
                </div> 
                
                
            </v-col>
        </v-row> 
    </div>
</template>

<script>
const axios = require('axios')

import io from "socket.io-client"
import { djangoServer } from '../base.js'

export default {
    name: 'ChatRoom',
    
    data() {
        return {
            room: { virtualId: '', name: ''},
            localPeer: { peerObject: null, peerId: null },
            socket: null,
            remotePeers: {},
            localAudioMedia: null,

            leave: false,

            roomMembers: [],
            roomMemberIds: [],

            message: null,
            messages: []
        }
    },

    created() {
        this.checkRouteParam()
    },

    methods: {
        // the first method to run when user navigate to the Chatroom page
        // to check if route is correct, eg: roomId, roomToken, ..
        checkRouteParam() {
            axios.get(djangoServer + 'api/check-route-param/', {
                params: {
                    id       : this.$route.params.roomId,
                    token    : this.$route.params.roomToken,
                    virtualId: this.$route.params.virtualId,
                    slug     : this.$route.params.slug,
                    ownerId  : this.$route.params.ownerId
                },
                headers: { 'Authorization': `Bearer ${this.$store.state.user.access}` }
            })
            .then((response) => {
                if (response.data['success']) {
                    // get user audio
                    this.getUserLocalAudioMedia()

                    this.room = response.data['room']

                    // add user as member 
                    if (this.$store.state.user.id != this.$route.params.ownerId) {
                        this.addRoomMember()
                    }
                    else this.getRoomMembers()

                    this.openNewPeerConnection()
                }
            })
            .catch(() => { this.$router.push({ name: 'Home' })})
        },

        getRoomMembers() {
            axios.get(djangoServer + 'api/get-room-members/', {
                params: { room_id: this.$route.params.roomId },
                headers: { 'Authorization': `Bearer ${this.$store.state.user.access}` }
            })   
            .then((response) => {
                this.roomMembers = response.data['members']
                this.roomMemberIds = []
                for (var i=0; i<this.roomMembers.length; i++) {
                    this.roomMemberIds.push(this.roomMembers[i]['id'])
                }
                this.getMessages()
            })
        },
 
        addRoomMember() {
            axios.post(djangoServer + 'api/add-new-member/', {
                room_id: this.$route.params.roomId,
                user_id: this.$store.state.user.id
            },
            {
                headers: { 'Authorization': `Bearer ${this.$store.state.user.access}` }
            })
            .then(() => { this.getRoomMembers() })
        },

        getUserLocalAudioMedia() {
            navigator.mediaDevices.getUserMedia({ audio: true })
            .then((media) => { 
                this.localAudioMedia = media 
                const audioElement = new Audio()
                this.addAudioStreamToDOM(audioElement, this.localAudioMedia, this.localPeer['peerId'], true)
            })
        },

        openNewPeerConnection() {
            this.localPeer['peerObject'] = new Peer()
            this.localPeer['peerObject'].on('open', (id) => { 
                this.localPeer['peerId'] = id 

                this.connectToSocketServer()

                // listen to call event from caller
                this.localPeer['peerObject'].on('call', (callConnection) => {
                    callConnection.answer(this.localAudioMedia)
                    callConnection.on('stream', (callerAudio) => {
                        const callerAudioElement = new Audio()
                        this.addAudioStreamToDOM(callerAudioElement, callerAudio, callConnection.peer, false)
                    })
                })
            })
            
        },

        connectToSocketServer() {
            this.socket = io('http://localhost:3000')

            this.socket.emit(
                'join-room', this.room.id, this.room.virtualId, this.room.ownerId, 
                this.$store.state.user.id, this.localPeer['peerId'], this.$store.state.user.access
            )

            // listen to user connect event
            this.socket.on('user-connected', (connectedUserPeerId) => {
                this.connectToNewUser(connectedUserPeerId, this.localAudioMedia)
            })      

            this.socket.on('user-disconnected', (userPeerId, userId) => {
                if (this.remotePeers[userPeerId]) this.remotePeers[userPeerId].close()

                if (this.$store.state.user.id == this.$route.params.ownerId) {
                    axios.post(djangoServer + 'api/remove-user-from-room/', {
                        room_id: this.$route.params.roomId,
                        user_id: userId
                    },
                    {
                        headers: { 'Authorization': `Bearer ${this.$store.state.user.access}` }
                    })
                    .then(() => { this.getRoomMembers() })
                }
                else {
                    setTimeout(() => { this.getRoomMembers() }, 1000)
                }
            })

            
            this.socket.on('end-call-connection', () => {
                this.leaveCall()
            })
            
            // listen to new message when user chat
            this.socket.on('new-message', (newMessage) => {
                for (var k=0; k<this.roomMembers.length; k++) {
                    if (this.roomMembers[k]['id'] == newMessage['senderId']) {
                        newMessage['avatarColor'] = this.roomMembers[k]['avatarColor']
                        newMessage['avatarName'] = this.roomMembers[k]['avatarName']
                    }
                }
                this.messages.push(newMessage)
            })
        },

        connectToNewUser(connectUserPeerId, audioStream) {
            const callConnection = this.localPeer['peerObject'].call(connectUserPeerId, audioStream)
            const audioElement = new Audio()
            // listen for answer and get answerer's audio back
            callConnection.on('stream', (answererAudioStream) => {
                this.addAudioStreamToDOM(audioElement, answererAudioStream, callConnection.peer, false)
            })

            callConnection.on('close', () => { audioElement.remove() })

            this.getRoomMembers()
            this.remotePeers[connectUserPeerId] = callConnection
        },

        addAudioStreamToDOM(audioElement, audioStream, userPeerId, local) {
            audioElement.srcObject = audioStream
            audioElement.id = `audio-${userPeerId}`
            audioElement.muted = local ? true : false
            audioElement.play()
            document.getElementById("audio-grid").appendChild(audioElement)
        },

        getMessages() {
            axios.get(djangoServer + 'api/get-messages/', {
                params: { room_id: this.$route.params.roomId },
                headers: { 'Authorization': `Bearer ${this.$store.state.user.access}` }
            })
            .then((response) => {
                this.messages = response.data['messages']

                if (this.messages.length > 0) {
                    for (var i=0; i < this.roomMembers.length; i++) {
                        for (var j=0; j < this.messages.length; j++) {
                            if (this.roomMembers[i]['id'] == this.messages[j]['senderId']) {
                                this.messages[j]['avatarColor'] = this.roomMembers[i]['avatarColor']
                                this.messages[j]['avatarName'] = this.roomMembers[i]['avatarName']
                            }
                            else if (!this.roomMemberIds.includes(this.messages[j]['senderId'])) {
                                this.messages[j]['avatarColor'] = "orange"
                                this.messages[j]['avatarName'] = this.messages[j]['senderName'][0]
                            }
                        }
                    }
                }
            })
        },

        sendMessage() {
            axios.post(djangoServer + 'api/send-message/', {
                room_id: this.$route.params.roomId,
                sender_id: this.$store.state.user.id,
                text: this.message
            },
            {
                headers: { 'Authorization': `Bearer ${this.$store.state.user.access}` }
            })
            .then((res) => {
                for (var k=0; k<this.roomMembers.length; k++) {
                    if (this.roomMembers[k]['id'] == res.data['message']['senderId']) {
                        res.data['message']['avatarColor'] = this.roomMembers[k]['avatarColor']
                        res.data['message']['avatarName'] = this.roomMembers[k]['avatarName']
                    }
                }
                this.messages.push(res.data['message'])
                this.socket.emit('send-new-message', res.data['message'])
            })
        },

        leaveCall() {
            this.$router.push({ name: 'Home' })
            window.location.reload()
        },

        endCall() {
            this.socket.emit("end-call")
            this.leaveCall()
        }
    }
}
</script>

<style scoped>
#users-card {
    border-right: 1px;
    border-right-style: solid;
    border-right-color: white;
    height: 100%;
}
</style>