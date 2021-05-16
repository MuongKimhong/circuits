<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12" class="col-lg-5 col-md-5 col-sm-6 mx-auto mt-5">
            
            <v-card align="center" class="px-5 py-5 mt-5 grey darken-4" flat>
                <h2 class="white--text">Sign Up</h2>

                <div v-if="error.show" class="red darken-3 py-2 mt-5" style="border-radius: 8px">
                  <h4 class="white--text">{{ error.text }}</h4>
                </div>

                <div v-if="showField" class="mt-3">
                  <v-text-field label="Username" type="text" v-model="username" color="#FFFFFF" dark></v-text-field>
                  <v-text-field label="Password" type="password" v-model="password1" color="#FFFFFF" dark></v-text-field>
                  <v-text-field label="Confirm Password" type="password" v-model="password2" color="#FFFFFF" dark></v-text-field>
                  <v-btn class="white text-capitalize col-12 mt-5" @click="register()">Sign Up</v-btn>

                  <div class="ml-auto mr-auto mt-5">
                      <v-btn text class="white--text text-capitalize" @click="$router.push({ name: 'Login' })">
                          already have an account
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
  name: "Register",
  data() {
    return {
      username: '',
      password1: '',
      password2: '',

      showField: true,

      error: {
        show: false,
        text: ''
      }
    }
  },
  methods: {
    register: function () {
      if (this.username == '' || this.password1 == '' || this.password2 == '') return;

      if (this.password1 != this.password2) {
        this.showField = true
        this.error.show = true
        this.error.text = "Two passwords didn't match"
        return;
      }

      this.showField = false
      this.error.show = false

      setTimeout(() => {
        axios.post(djangoServer + 'api/bcaou3gcauklbv3/register/', {
          username: this.username,
          password: this.password1
        })
        .then((response) => {
          if (response.data['success']) this.$router.push({ name: 'Login' })
        })
        .catch((error) => {
          if (error.response.data['username_taken']) {
            this.showField = true
            this.error.show = true
            this.error.text = "Username is already taken"
          }
        })
      }, 1000)
    }
  }
};
</script>

<style scoped>
</style>