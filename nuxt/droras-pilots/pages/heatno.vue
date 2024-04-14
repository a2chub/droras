<template>
  <div class="bg">
    <div class="heat-index">
      {{ heatIndex }}
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    heatIndex () {
      return this.$store.state.current.heat
    }
  },
  created () {
    this.$store.dispatch('initRaces')
    this.$store.dispatch('initCurrent')
  }
}
</script>

<style>
html, body, #__nuxt, #__layout {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: black;
}
.heat-index {
  color: white;
  font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
  text-align: center;
  font-size: 40px;
  font-weight: bold;
  position: absolute;
  top: 10px;
  left: 20px;
}
</style>
