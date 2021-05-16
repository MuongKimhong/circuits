<template>
  <v-app>
    <v-app-bar
      app
      class="grey darken-4"
    >
      <div class="d-flex align-center">
        <v-btn text >
          <h1 class="white--text">Circuits</h1>
        </v-btn>
      </div>

      <v-spacer></v-spacer>

      <v-btn text v-if="$store.state.user != null">
        <span class="mr-2 white--text">{{ $store.state.user.username }}</span>
      </v-btn>
      <v-btn text v-if="$store.state.user != null" @click="logout()">
        <span class="mr-2 white--text">Logout</span>
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  methods: {
    logout() {
      this.$store.commit('deleteUserInfo')
      this.$router.push({ name: 'Login' })
    },

    logoClick () {
      this.$router.push({ name: 'Home' })
      window.location.reload()
    }
  }
};
</script>

<style>
h1, h2, h3, h4, h5, h6, button, p, small, span {
  font-family: 'Roboto', sans-serif;
}
#app {
  background-color: rgb(34, 34, 34);
}
</style>