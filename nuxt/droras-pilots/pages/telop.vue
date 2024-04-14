<template>
  <div class="bg">
    <div
      v-for="(pilot, index) in pilots"
      :key="index"
      class="name"
    >
      {{ pilot.name }}
    </div>
    <div class="heat-index">
      {{ heatIndex }}
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    pilots () {
      const current = this.$store.state.current ? this.$store.state.current.heat | 0 : 0
      return this.$store.state.heats.filter((heat, index) => index + 1 === current)[0]
    },
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
.bg {
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
}
.name {
  color: white;
  width: 33.3333%;
  font-family: sans-serif;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  margin-top: 20px;
}
.heat-index {
  color: white;
  font-family: sans-serif;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  position: absolute;
  top: 20px;
  left: 10px;
}
</style>
