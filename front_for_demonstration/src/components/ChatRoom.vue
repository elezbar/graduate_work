<template lang="pug">
div
  v-sheet.pb-8.mx-auto(width="1200")
    v-slider(
      v-model="slider"
      color="orange darken-3"
      label="Progress"
      min="0"
      max="1000"
      @change="sliderChange"
    )
    v-btn.mt-2(type="submit" @click="playPause" block) {{ play_pause }}
  v-sheet.mx-auto.mb-10(width="300")
    v-form(@submit.prevent)
      v-text-field(
        v-model="message"
        label="New Message")
      
      v-btn(type="submit" @click="sendMessage" block class="mt-2") Send Message
  v-sheet.mx-auto.chat#chat(width="400" height="400")
    p(v-for="obj in chat")
      strong {{ obj.username }}:&nbsp;
      span {{ obj.message }}
</template>
  
<script>
  export default {
    name: 'TheRoom',
    data: () => ({
      roomname: null,
      message: null,
      play_pause: "Play",
      connection: null,
      slider: 0,
      interval: null,
      chat: []
    }),
    created () {
      this.roomname = this.$route.params.roomname
      this.username = this.$route.query.username
      this.connection = new WebSocket("ws://localhost:8002/" + this.roomname)

      let context = this
      this.connection.onmessage = function(event) {
        var obj = JSON.parse(event.data);
        console.log(obj)
        if (obj.username != context.username) {
          if (obj.type == 'slider') {
            context.slider = obj.value
          } else if (obj.type == 'play') {
            context.playItNow()
          } else if (obj.type == 'pause') {
            context.pauseItNow()
          } else if (obj.type == 'message') {
            context.writeToChat(obj.username, obj.message)
          }
        }
        if (obj.type == 'initial_response' && obj.username == context.username) {
          console.log('initial_response', obj)
          context.slider = obj.slider
          if (obj.condition == 'play') {
            context.playItNow()
          }
          if (obj.condition == 'pause') {
            context.pauseItNow()
          }
          context.chat = obj.chat
          context.slider = obj.slider
        }
      }
      this.connection.onopen = function() {
        context.sendInitial()
      }
    },
    updated () {
      this.fixChatPosition()
    },
    activated () {
      this.fixChatPosition()
    },
    beforeDestroy () {
      this.connection.close()
    },
    methods: {
      sendInitial() {
        let msg = JSON.stringify({
          type: 'initial_request',
          token: 'scdasdc',
          username: this.username
        });
        this.connection.send(msg);
        console.log('initial_request')
      },
      sliderChange() {
        let msg = JSON.stringify({
          type: 'slider',
          value: this.slider,
          token: 'scdasdc',
          username: this.username
        });
        this.connection.send(msg);
      },
      sliderChangeInfo() {
        let msg = JSON.stringify({
          type: 'slider_info',
          token: 'scdasdc',
          value: this.slider
        });
        this.connection.send(msg);
      },
      sendMessage () {
        let msg = JSON.stringify({
          type: 'message',
          username: this.username,
          token: 'scdasdc',
          message: this.message
        });
        this.connection.send(msg);
        this.writeToChat(this.username, this.message)
        this.message = null
      },
      writeToChat (username, message) {
        this.chat.push({
          username: username,
          message: message,
        })
        this.fixChatPosition()
      },
      fixChatPosition () {
        var chat = document.getElementById("chat")
        console.log("chat.scrollHeight", chat.scrollHeight, chat.scrollHeight + 200)
        setTimeout(() => {chat.scrollTop = chat.scrollHeight + 50}, 10)
      },
      playItNow () {
        this.play_pause = "Pause"
        this.interval = setInterval(() => {
          this.slider += 5
          this.sliderChangeInfo()
        }, 1000);
      },
      pauseItNow () {
        this.play_pause = "Play"
        clearInterval(this.interval)
      },
      playPause () {
        if (this.play_pause == "Play") {
          let msg = JSON.stringify({type: 'play', token: 'scdasdc', username: this.username});
          this.connection.send(msg);
          this.playItNow()
        } else {
          let msg = JSON.stringify({type: 'pause', token: 'scdasdc', username: this.username});
          this.connection.send(msg);
          this.pauseItNow()
        }
      }
    }
  }
</script>
  
<style scoped lang="sass">
  .chat
    overflow-y: scroll
    overflow-x: hidden
    padding: 5px
    border-radius: 10px
    border: 1px solid #eee
    display: flex
    flex-direction: column
    flex-wrap: nowrap
    p
      margin-bottom: 7px
      max-width: 350px
      text-align: left
      span.datetime
        color: #bbb
  .chat > :first-child
    margin-top: auto !important
</style>
