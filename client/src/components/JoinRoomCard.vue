<template>
    <div>
        <v-col cols=12 class="col-lg-5 col-md-5 col-sm-6 mt-5 mx-auto">
            <v-card flat class="mt-5 px-5 py-5 grey darken-3" align="center">

                <div v-if="error.show" class="red darken-3 py-2 mt-5" style="border-radius: 8px">
                  <h4 class="white--text">{{ error.text }}</h4>
                </div>

                <v-text-field label="Enter room id" v-model="virtualId" type="text" color="#FFFFFF" dark class="mt-5">
                </v-text-field>
                <v-text-field v-if="hasPassword" v-model="password" label="Enter room password" type="password" color="#FFFFFF" dark>
                </v-text-field>

                <div v-if="check">
                    <v-btn class="white text-capitalize col-12 mt-2" @click="checkPassword()">Join room</v-btn>
                </div>
                <div v-else>
                    <v-btn class="white text-capitalize col-12 mt-2" @click="joinRoom()">Join room</v-btn>
                </div>
                
                <div class="ml-auto mr-auto mt-4">
                    <v-btn text class="white--text text-capitalize py-0" @click="$emit('create')">
                        Create room
                    </v-btn>
                </div>
                
            </v-card>
        </v-col>
    </div>
</template>

<script>
const axios = require('axios')
import { djangoServer } from '../base.js'

export default {
    name: 'JoinRoomCard',

    data() {
        return {
            hasPassword: false,
            check: true,

            error: {
                show: false,
                text: ''
            },

            virtualId: '',
            password: ''
        }
    },

    methods: {
        checkPassword () {
            this.error.show = false

            axios.get(djangoServer + 'api/check-password/', {
                params: {
                    virtualId: this.virtualId
                },
                headers: { 'Authorization': `Bearer ${this.$store.state.user.access}` } 
            })
            .then((response) => {
                // if has password
                if (!response.data['no_password']) {
                    this.hasPassword = true
                    this.check = false 
                } 
                else {
                    this.joinRoom()
                }
            })
            .catch((error) => {
                if (error.response.data['error']) {
                    this.error.show = true
                    this.error.text = "Room doesn't exists"
                }
            })
        },
        joinRoom () {
            if (this.virtualId == '') return;

            this.error.show = false

            axios.post(djangoServer + 'api/join-room/', {
                virtualId: this.virtualId,
                password: this.password,
                user_id: this.$store.state.user.id
            },
            {
                headers: { 'Authorization': `Bearer ${this.$store.state.user.access}` } 
            })
            .then((response) => {
                var data = response.data['room']
                this.$router.push({ name: 'ChatRoom', params: {
                    slug: data.slug, roomToken: data.token, roomId: data.id, virtualId: data.virtualId,
                    ownerId: data.ownerId
                }}) 
            })
            .catch((error) => {
                if (error.response.data['errorPassword']) {
                    this.error.show = true
                    this.error.text = "Password is incorrect"
                }
            })
        }
    }    
}
</script>

<style>
.v-label {
    color: white
}
</style>