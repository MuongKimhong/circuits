<template>
  <div>
    <v-container v-if="showHomePage">
      <v-col cols=12 class="mt-5">
          <v-row class="mt-5">
            <v-col cols=12 class="col-lg-6 col-md-6 col-sm-12">
              <v-btn class="green accent-4 col-12 px-5 py-5 text-capitalize" style="height: 100px"
                     @click="createRoom()">
                <h1>Create new room</h1>
              </v-btn>
            </v-col>
            <v-col cols=12 class="col-lg-6 col-md-6 col-sm-12">
              <v-btn class="cyan accent-4 col-12 px-5 py-5 text-capitalize" style="height: 100px"
                     @click="joinRoom()">
                <h1>Join room</h1>
              </v-btn>
            </v-col>
          </v-row>
      </v-col>

      <div style="margin-top: 100px">
        <h2 align="center" class="white--text mt-5">Current rooms online: {{ roomsOnline }}</h2>
      </div>

    </v-container>

    <div v-if="showCreateRoom">
      <CreateRoomCard v-on:join="joinRoom"/>
    </div>

    <div v-if="showJoinRoom">
      <JoinRoomCard v-on:create="createRoom"/>
    </div>
  </div>
</template>

<script>
  import CreateRoomCard from '../components/CreateRoomCard.vue'
  import JoinRoomCard from '../components/JoinRoomCard.vue'
  import { djangoServer } from '../base.js'
  const axios = require('axios')

  export default {
    name: 'Home',
    components: {
      CreateRoomCard,
      JoinRoomCard
    },
    data() {
      return {
        showHomePage: true,
        showCreateRoom: false,
        showJoinRoom: false,

        roomsOnline: 0,
        interval: null
      }
    },
    created () {
      this.getRoomOnline()
      var self = this
      this.interval = setInterval(function () { self.getRoomOnline() }, 2000)
    },

    beforeRouteLeave (to, from, next) {
      clearInterval(this.interval)
      next()
    },
    methods: {
      createRoom () {
        this.showHomePage = false
        this.showJoinRoom = false
        this.showCreateRoom = true
      },
      joinRoom () {
        this.showHomePage = false
        this.showJoinRoom = true
        this.showCreateRoom = false
      },
      getRoomOnline () {
        console.log("hello")
        axios.get(djangoServer + 'api/room-count/')
        .then((res) => { this.roomsOnline = res.data['rooms'] })
      }
    }
  }
</script>
