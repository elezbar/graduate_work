<template lang="pug">
div
  v-sheet.mx-auto(width="300")
    v-form(@submit.prevent)
      v-text-field(
        v-model="roomName"
        label="Room name")

      v-text-field(
        v-model="yourName"
        label="Your name")

      v-text-field(
        v-model="yourName"
        label="Your name")
      
      v-btn(type="submit" @click="Connect" block class="mt-2") Connect
  
</template>
  
<script>
  import ChatRoom from './ChatRoom.vue'
  
  export default {
    name: 'App',
    components: {
      ChatRoom
    },
    data: () => ({
      roomName: null,
      yourName: null
    }),
    methods: {
      Connect () {
        if (this.roomName && this.yourName) {
          this.$router.push('/chatroom/' + this.roomName + "/?username=" + this.yourName)
        }
      },

    }
  }
</script>
  
<style lang="sass">
  #app
    font-family: Avenir, Helvetica, Arial, sans-serif
    -webkit-font-smoothing: antialiased
    -moz-osx-font-smoothing: grayscale
    text-align: center
    color: #2c3e50
    margin-top: 60px
</style>
  