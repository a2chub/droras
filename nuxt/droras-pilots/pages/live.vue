<template>
  <div class="bg">
    <div class="video">
      <video autoplay></video>
    </div>
    <div
      v-for="(pilot, index) in pilots"
      :key="index"
      class="name"
    >
      {{ pilot.name }}
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    pilots () {
      const current = this.$store.state.current.heat | 0
      return this.$store.state.heats.filter((heat, index) => index + 1 === current)[0]
    }
  },
  created () {
    this.$store.dispatch('initRaces')
    this.$store.dispatch('initCurrent')
  }
}

function hasGetUserMedia () {
  return !!(navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia)
}

if (hasGetUserMedia()) {
} else {
  alert('getUserMedia() is not supported in your browser')
}
// ------------------------------------------------------
const onFailSoHard = function (e) {
  // console.log('Reeeejected!', e)
}

// Not showing vendor prefixes.
navigator.getUserMedia('video, audio', function (localMediaStream) {
  const video = document.querySelector('video')
  video.src = window.URL.createObjectURL(localMediaStream)

  // Note: onloadedmetadata doesn't fire in Chrome when using it with getUserMedia.
  // See crbug.com/110938.
  video.onloadedmetadata = function (e) {
    // Ready to go. Do some stuff.
  }
}, onFailSoHard)
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
</style>
