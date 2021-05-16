<template>
    <div>
        <v-col cols=12 class="col-lg-5 col-md-5 col-sm-6 mt-5 mx-auto">
            <v-card flat class="mt-5 px-5 py-5 grey darken-3" align="center">

                <div v-if="error.show" class="red darken-3 py-2 mt-5" style="border-radius: 8px">
                  <h4 class="white--text">{{ error.text }}</h4>
                </div>

                <v-text-field label="Enter room name" v-model="name" type="text" color="#FFFFFF" dark class="mt-5">
                </v-text-field>
                <v-text-field v-if="setPassword" v-model="password" label="Enter room password" type="password" color="#FFFFFF" dark>
                </v-text-field>
                <v-row>
                    <v-checkbox color="white" class="ml-2" @change="setPassword = !setPassword"></v-checkbox>
                    <span class="mt-5 white--text">Set password</span>
                </v-row>

                <div>
                    <v-btn class="white text-capitalize col-12 mt-2" @click="createNewRoom()">Create room</v-btn>
                </div>
                
                <div class="ml-auto mr-auto mt-4">
                    <v-btn text class="white--text text-capitalize py-0" @click="$emit('join')">
                        Join room
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
    name: 'CreateRoomCard',

    data() {
        return {
            setPassword: false,

            error: {
                show: false,
                text: ''
            },

            name: '',
            password: ''
        }
    },

    methods: {
        createNewRoom () {
            if (this.name == '') return;
            
            this.error.show = false

            axios.post(djangoServer + 'api/create-new-room/', {
                user_id: this.$store.state.user.id,
                name: this.name,
                password: this.password
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
            .catch(() => {
                this.error.show = true
                this.error.text = "Room name already taken"
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