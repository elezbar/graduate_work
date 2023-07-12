<template lang="pug">

v-container
  .until
    span Battle ends in:
  v-row.pt-4(justify="center")
    v-col(cols="12")
      v-row.pt-4(justify="center")
        v-col.d-flex.justify-center.align-center.pt-10.pb-10(cols="12")
          .lent_wrap
            .lent_top
            .lent_bot
            .lent_left
            .lent_right
            .lent_left_col
              img.width90(src="@/assets/fan-fight.svg")
            .fist_wrap
              #countdown.countdown
                .countdown-number.day
                  span.days.countdown-time.score
                  span.countdown-text D
                .countdown-number.hour
                  span.hours.countdown-time.score
                  span.countdown-text H
                .countdown-number.min
                  span.minutes.countdown-time.score
                  span.countdown-text M
                .countdown-number.sec
                  span.seconds.countdown-time.score
                  span.countdown-text S
            .lent_right_col
              img.width100(src="@/assets/support.svg")

      v-row.d-flex.justify-center.align-stretch.logos_wrap
        v-col.d-flex.justify-center.align-center(cols="12")
          v-col.d-flex.justify-center.align-center.flex-wrap.pos_r(md="4" sm='4' cols='5')
            img.width100(src="@/assets/manchester.svg")
            div.width100.ta_center.mob_counter.counter_left.score <!--img class="counter_icon" src="@/assets/counter.svg" width="22px"--><strong class="counter_num">{{manchester}}</strong>
          v-col.d-flex.justify-center.align-center.flex-wrap(md="4" sm='4' cols='2')
            .mt-10
              span.width100.vs.ta_center.pb-2 VS
            div.mb-0.text-center.counter.width100.d_flex.justify-center.pos_r
              div.counter_left.ta_right <strong class="counter_num score">{{manchester}}</strong>
              div.two_dots
              div.counter_right.ta_left <strong class="counter_num score">{{liverpool}}</strong>
          v-col.d-flex.justify-center.align-center.flex-wrap.pos_r(md="4" sm='4' cols='5')
            img.width90(src="@/assets/liverpool.svg")
            div.width100.ta_center.mob_counter.counter_right.score <!--img class="counter_icon" src="@/assets/counter.svg" width="22px"--><strong class="counter_num">{{liverpool}}</strong>

      v-row.d-flex.justify-center.align-start.buttons_wrap.pos_r
        v-col.d-flex.justify-center.align-center(md="4" sm='4' cols='5')
          v-btn.button(color="success" v-if="!voted" block x-large @click="vote(manchester_id)") Support Manchester!
          v-btn.button(color="disabled" v-else block x-large @click="already_voted") Thanks for your vote!
        v-col.pos_r(md="4" sm='4' cols='2')
          img.cup(src="@/assets/cup.svg")
        v-col.d-flex.justify-center.align-center(md="4" sm='4' cols='5')
          v-btn.button(color="success" v-if="!voted" block x-large @click="vote(liverpool_id)") Support Liverpool!
          v-btn.button(color="disabled" v-else block x-large @click="already_voted") Thanks for your vote!

      v-row.mt-12.d-flex.justify-center.align-stretch
        v-col.d-flex.justify-center.align-center.mt-0.mb-0.pt-0.pb-0(cols="2")
          img.width100.boots(src="@/assets/boots.svg")

      v-row.mt-8.d-flex.justify-center.align-stretch
        v-col.d-flex.justify-center.align-center(cols="12")
          h2.text-center.width100.mb-0.fz-22 Help your club win — share the link with your friends!
        v-col.d-flex.justify-center.align-center(cols="12")
          // .ya-share2.pl-0(
          //   data-curtain
          //   data-size="l"
          //   data-shape="round"
          //   data-services="vkontakte,odnoklassniki,telegram,twitter,whatsapp,moimir,skype,reddit"
          //   data-title="Битва фанатов: Спартак (Мск) – Зенит (СПб)."
          //   data-image="https://bitva.fun/media/foot_bg.jpg"
          //   data-description="Уникальный эксперимент определит кто круче. Поддержи свой клуб в один клик!"
          // )
          .sharethis-inline-share-buttons

      v-row.mt-7.mb-0(justify="center")
        v-col
          .note.d-flex
            v-col.d-flex.justify-center.align-center.note_left(cols="2")
              img.ball.width90(src="@/assets/football.svg")
            v-col.note_middle(cols="8")

              p.body-2.mb-3 This survey is conducted by an initiative fan to find a fair answer whose football club fans are more united and better. 
                | The battle will be finished on 1st of June. The club with the most active fans will win.

              p.body-2.mb-0 One fan can vote only once. To help your favorite club win, 
                | invite as many of your fan friends as possible to this survey by any means (social networks, instant messengers, e-mail, etc.).

            v-col.d-flex.justify-center.align-center.note_right(cols="2")
              img.ball.width90(src="@/assets/timer.svg")

      v-row.mt-0.mb-2.d-flex.justify-center.align-stretch
        v-col.d-flex
          v-col.d-flex.justify-center.align-center(cols="2")
          v-col.d-flex.justify-center.align-center(cols="8")
            p.small_text.body-2.mb-0 * All logos on this website are registered trademarks 
              | of their respective football clubs and are not used for commercial purposes.
              | This sociological survey is exclusively scientific in nature, and logos are
              | used only for informational purposes (for visual identification of FC, etc.). 
              | Contact us: <a href="mailto:info@fanbattle.fun">info@fanbattle.fun</a>
          v-col.d-flex.justify-center.align-center(cols="2")

</template>


<script>
  import { initializeClock, setVote, getVotes } from "@/service/service"
  export default {
    name: 'FirstVersion',

    data: () => ({
      voted: false,
      liverpool_id: 4,
      manchester_id: 3,
      liverpool: 0,
      manchester: 0
    }),
    created () {
      this.check_is_voted()
      this.get_votes()
    },
    mounted () {
      let deadline = "June 01 2023 00:00:00 GMT+0300"
      initializeClock('countdown', deadline)
      setInterval(this.get_votes, 3000)
      setInterval(this.check_is_voted, 1000)
    },

    methods: {
      async vote (club) {
        let data = await setVote({"club": club})
        this.$swal({
          "icon": "success",
          "title": "Your vote has been counted, thanks!",
          "text": "Invite your friends to help your club win!",
        })
        this.voted = true
        this.liverpool = data["liverpool"]
        this.manchester = data["manchester"]
        this.$cookies.set("voted", "true")
        localStorage.setItem("voted", "true")
        sessionStorage.setItem("voted", "true")
      },
      async get_votes () {
        let data = await getVotes()
        this.liverpool = data["liverpool"]
        this.manchester = data["manchester"]
      },
      check_is_voted () {
        if (this.$cookies.get("voted")) {
          localStorage.setItem("voted", "true")
          sessionStorage.setItem("voted", "true")
          this.voted = true
        } else if (localStorage.getItem("voted")) {
          this.$cookies.set("voted", "true")
          sessionStorage.setItem("voted", "true")
          this.voted = true
        } else if (sessionStorage.getItem("voted")) {
          this.$cookies.set("voted", "true")
          sessionStorage.setItem("voted", "true")
          this.voted = true
        } else if (this.voted) {
          this.$cookies.set("voted", "true")
          localStorage.setItem("voted", "true")
          sessionStorage.setItem("voted", "true")
        }
      },
      already_voted() {
        this.$swal({
          "icon": "warning",
          "title": "You have already voted.",
          "text": "Invite your friends to help your club win!",
        })
      }
    }
  }
</script>

<style lang="sass">

.cup
  position: absolute
  top: -25px
  width: 70px
  left: 50%
  margin-left: -35px
  @media (max-width: 1100px)
    top: -10px
    width: 60px
    left: 50%
    margin-left: -30px
  @media (max-width: 700px)
    top: 20px
    width: 40px
    left: 50%
    margin-left: -20px

@font-face
  font-family: 'Agency'
  src: url('@/assets/agencyfb_reg.ttf') format('truetype')

.score
  font-family: 'Agency', sans-serif

.swal-title, .swal-text
  font-family: 'Roboto', sans-serif

.until
  position: absolute
  top: 0
  left: 50%
  margin-left: -130px
  width: 260px
  height: 30px
  line-height: 30px
  background-color: #b1b1b1
  text-align: center
  span
    color: #fff
  &:before, &:after
    position: absolute
    box-sizing: border-box
    top: 0px
    content: ""
    display: block
    border-bottom: 35px solid #fff
    border-top: 0px solid white
    border-style: solid
    background: #b1b1b1
    width: 0px
    height: 0px
    left: -35px
    border-left: 0px solid #fff
    border-right: 35px solid #b1b1b1
  &:after
    border-left: 35px solid #b1b1b1
    border-right: 0px solid #fff
    left: auto
    right: -35px


.button
  padding: 0 5px !important
  flex: auto !important
  white-space: normal
  .v-btn__content
    flex: auto !important
    @media (max-width: 600px)
      flex: auto !important
      letter-spacing: normal
      font-size: 15px

.lent_wrap
  width: calc(100% - 146px)
  height: 130px
  position: relative
  height: 117px
  background-color: #939393
  opacity: 0.85
  @media (max-width: 600px)
    width: 100%
    height: 70px
    &:after, &:before
      content: ""
      display: block
      width: 50px
      top: 0
      position: absolute
      left: -50px
      height: 100%
      background-color: #939393
    &:before
      left: initial
      right: -50px

  .lent_left_col, .lent_right_col
    width: calc(50% - 150px)
    height: 100%
    position: absolute
    display: flex
    align-items: center
    top: 0
    @media (max-width: 800px)
      width: calc(50% - 120px)
    @media (max-width: 600px)
      width: calc(50% - 80px)
    img
      max-width: 200px
    h1
      font-family: 'Roboto', sans-serif
      font-style: italic
      font-size: 40px
      color: #fff
      text-transform: uppercase
      line-height: 42px

  .lent_left_col
    justify-content: flex-start
    left: 0
    @media (max-width: 600px)
      width: calc(50% - 110px)

  .lent_right_col
    justify-content: flex-end
    right: 0
    img
      max-width: 275px
    
  .lent_top
    height:20px
    position: absolute
    top: 0
    left: 0
    width: 100%
    background: url(@/assets/lent_top.svg)
    background-position: top center
    background-repeat: no-repeat
  
  .lent_bot
    height:20px
    position: absolute
    bottom: 0
    left: 0
    width: 100%
    background: url(@/assets/lent_bot.svg)
    background-position: bottom center
    background-repeat: no-repeat
  
  .fist_wrap
    position: absolute
    width: 300px
    height: 200px
    top: 50%
    margin-top: -90px
    left: 50%
    margin-left: -152px
    background: url(@/assets/fist.svg)
    background-position: center center
    background-repeat: no-repeat
    background-size: 100%
    z-index: 1
    display: flex
    align-items: center
    @media (max-width: 600px)
      transform: scale(0.6)

  .lent_left
    position: absolute
    width: 73px
    height: 130px
    left: -73px
    top: 0
    background: url(@/assets/lent_l.svg)
    background-position: top right
    background-repeat: no-repeat
    @media (max-width: 600px)
      display: none

  .lent_right
    position: absolute
    width: 73px
    height: 130px
    right: -73px
    top: 0
    background: url(@/assets/lent_r.svg)
    background-position: top left
    background-repeat: no-repeat
    @media (max-width: 600px)
      display: none

.counter
  padding: 5px
  min-height: 70px
  
  div
    line-height: 50px
  @media (max-width: 800px)
    padding: 0px
  @media (max-width: 600px)
    display: none !important
  .counter_left, .counter_right
    height: 66px
    display: flex
    justify-content: end
    align-items: center
    width: calc(50% - 7px)
    border: 5px solid #d8d8d8
    background-color: #f5f5f5
    border-radius: 10px
    margin-right: 7px
    padding-right: 10px
  .counter_right
    justify-content: start
    margin-right: auto
    margin-left: 7px
    padding-right: 0px
    padding-left: 10px
  @media (max-width: 800px)
    .counter_left
      padding-right: 5px
    .counter_right
      padding-right: 0px
      padding-left: 5px
  

.buttons_wrap
  padding-top: 12px
  @media (max-width: 600px)
    padding-top: 0
    margin-top: 0
  @media (max-width: 600px)
    &:before, &:after
      content: ""
      width: 6px
      height: 6px
      display: block
      position: absolute
      left: 50%
      margin-left: -3px
      background: #000
      bottom: 145px
      border-radius: 6px
    &:after
      bottom: 132px

.counter_icon
  width: 25px
  display: inline-block
  position: relative
  top: 5px
  opacity: 0.8
  margin-right: 5px

.counter_num
  font-size: 45px
  @media (max-width: 800px)
    font-size: 30px

.mob_counter
  display: none
  margin-top: 10px
  @media (max-width: 600px)
    display: flex
.mob_counter.counter_left, .mob_counter.counter_right
  position: relative
  height: 50px
  line-height: auto
  align-items: center
  width: 100%
  border: 5px solid #d8d8d8
  background-color: #f5f5f5
  border-radius: 10px
  padding-right: 10px
  padding-left: 3px
  margin-right: 0
  justify-content: end
.mob_counter.counter_right
  padding-right: 3px
  padding-left: 10px
  margin-right: auto
  margin-left: 0
  justify-content: start

img.boots
  max-width: 150px !important
  min-width: 80px !important

.note
  filter: grayscale(1)
  background-color: #e0d4e3
  border-radius: 15px
  padding: 0 15px
  p
    padding: 15px 25px
    border-radius: 10px
    background-color: #fcf2ff
  @media (max-width: 600px)
    .note_middle
      flex: auto !important
      max-width: initial !important
      width: 100% !important
    .note_left, .note_right
      display: none !important

.vs
  font-size: 3.5em
  font-weight: 600
  display: inline-block
  color: #707070
  @media (max-width: 600px)
    font-size: 2.5em
    position: relative
    top: -40px

.container
  max-width: 1200px

.countdown-title
  color: #396
  font-weight: 100
  font-size: 40px
  margin: 40px 0px 20px

.countdown
  font-family: sans-serif
  color: #222
  display: inline-block
  font-weight: 100
  text-align: center
  font-size: 26px
  filter: grayscale(1)
  width: 300px
  .day
    left: -1px
  .hour
    left: -6px
  .min
    left: -5px
  .sec
    left: -3px

.countdown-number
  position: relative
  padding: 2px
  border-radius: 3px
  display: inline-block
  min-width: 48px
  margin: 0 1px
  line-height: 1.2

.countdown-time
  padding: 2px
  border-radius: 3px
  background: transparent
  display: inline-block
  width: 100%

.countdown-text 
  display: block
  padding-top: 0
  font-size: 14px
  font-weight: 500
  color: #222

.two_dots
  position: absolute
  top:0
  left: 50%
  margin-left: -3px
  width: 6px
  height: 100%
  color: #000
  &:before, &:after
    content: ''
    display: block
    width: 8px
    height: 8px
    background: #000
    border-radius: 5px
    position: absolute
    left: -1px
    top: 27px
    opacity: 1
    @media (max-width: 800px)
      top: 21px
  &:after
    top: 42px
    @media (max-width: 800px)
      top: 36px

.v-application
  p.small_text
    padding: 0 10px
    font-size: 12px !important
    color: #b3b3b3

.v-btn
  height: 66px !important

img.width100
  max-width: 400px

img.ball.width90
  width: 90%
  max-width: 100px

h2.fz-22
  font-size: 22px !important

.width100
  width: 100%

.width90
  width: 90%

.width50
  width: 50%

.ta_center
  text-align: center

.ta_right
  text-align: right

.ta_left
  text-align: left

.pos_r
  position: relative

.d_flex
  display: flex

.st-remove-label[data-network=telegram]
  display: inline-block !important

#st-1
  z-index: 1 !important

</style>
