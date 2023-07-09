<template lang="pug">

v-container
  
  img.width50(src="@/assets/fan-fight.svg")
  img.width50(src="@/assets/support.svg")

  .tablo.d-flex.align-center.justify-center.flex-wrap
    .timer_wrap.width100.ta_center.align-top.justify-center.flex-wrap
      span До конца голосования осталось
      #countdown.countdown
        .countdown-number.day
          span.days.countdown-time
          span.countdown-text Дн.
        .countdown-number.hour
          span.hours.countdown-time
          span.countdown-text Час.
        .countdown-number.min
          span.minutes.countdown-time
          span.countdown-text Мин.
        .countdown-number.sec
          span.seconds.countdown-time
          span.countdown-text Сек.
    .round.round_zenit
      img(src="@/assets/zenit.svg")
    .vs VS
    .round.round_spartak
      img(src="@/assets/spartak.svg")

    
  
  // v-row.d-flex.justify-center.align-stretch.mt-6
  //   v-col.d-flex.justify-center.align-center(cols="12")
  //     v-col.d-flex.justify-center.align-center.flex-wrap.tablo(md="12" sm='8' cols='8')


</template>
  
  
  <script>
    //import { initializeClock } from "@/service/service"
    export default {
      name: 'NewVersion',
  
      data: () => ({
  
      }),
  
      mounted () {
        //var deadline="December 01 2022 00:00:00 GMT+0300";
        //initializeClock('countdown', deadline);
      }
    }
  </script>
  
<style lang="sass" scoped>

  .tablo
    background-color: rgba(255, 255, 255, 0.4)
    height: 500px
    border: 1px solid transparent
    border-image: linear-gradient(#ffffffcc, #00ffe07a)
    border-image-slice: 1
  
  .round
    width: 200px
    height: 200px
    border-radius: 300px
    background: rgba(255, 255, 255, 0.9)
    border: 5px solid #ffd200
    box-shadow: 0px 0px 15px 0px #000
    display: flex
    align-items: center
    justify-content: center
    img
      width: 100%

  .vs
    font-size: 3em
    padding: 0 20px
    color: #e9ffa5
    text-shadow: 0px 0px 10px #000
    
  .round_zenit
    border-color: #00afef

  .round_spartak
    border-color: #c8102e
  
  .v-application
    background-color: transparent !important
  
  body
    background: url('@/assets/foot_bg.jpg') no-repeat center center fixed !important 
    background-size: cover !important
    background-color: #000 !important

</style>
  