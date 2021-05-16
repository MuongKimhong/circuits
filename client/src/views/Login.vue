<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12" class="col-lg-5 col-md-5 col-sm-6 mx-auto mt-5">
            
            <v-card align="center" class="px-5 py-5 mt-5 grey darken-4" flat>
                <h2 class="white--text">Sign In</h2>

                <div v-if="error.show" class="red darken-3 py-2 mt-5" style="border-radius: 8px">
                  <h4 class="white--text">{{ error.text }}</h4>
                </div>  

                <div v-if="showField" class="mt-5">
                  <v-text-field label="Username" type="text" v-model='username' color="#FFFFFF" dark></v-text-field>
                  <v-text-field label="Password" type="password" v-model="password" color="#FFFFFF" dark></v-text-field>
                  <v-btn class="white text-capitalize col-12 mt-5" @click="login()">Sign in</v-btn>

                  <div class="ml-auto mr-auto mt-5">
                      <v-btn text class="white--text text-capitalize" @click="$router.push({ name: 'Register' })">
                          Create new Account
                      </v-btn>
                  </div>
                </div>

                <div v-else class="mt-5">
                  <v-progress-circular :size="60" :width="5" indeterminate color="white" class="mt-5"></v-progress-circular>
                </div>

            </v-card>

        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
const axios = require('axios')

import { djangoServer } from '../base.js'

export default {
  name: "Login",

  data() {
    return {
      username: '',
      password: '',

      showField: true,

      error: {
        show: false,
        text: ''
      }
    }
  },

  methods: {
    login: function () {
      if (this.username == '' || this.password == '') return;

      this.showField = false
      this.error.show = false

      setTimeout(() => {
        axios.post(djangoServer + 'api/oq8va034o02cv26v2ckga/token-obtain/2lbcooo297cb19uz/', {
          username: this.username,
          password: this.password
        })
        .then((response) => {
          this.$store.commit('getUserInfo', response.data)
          this.$router.push({ name: 'Home' })
        })
        .catch((error) => {
          console.log(error.response)
          this.showField = true
          this.error.show = true
          this.error.text = "Username or password is incorrect"
        })
      }, 1000)
    }
  }
};
</script>

<style scoped>
</style>