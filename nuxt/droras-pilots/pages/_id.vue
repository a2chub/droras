<template lang="pug">
  .container
    table.table
      thead
        tr
          th Heat
          th Class
          th E1: 5705
          th F1: 5740
          th F4: 5800
      tbody.list
        tr(v-for='heat in heats'
          :key='heat.index'
          :class='{ "table-success": heat.active, "active": heat.active }')
          td {{ heat.index }}
          td {{ heat.class }}
          td(v-for='(pilot, pilotindex) in heat.pilots' :key='pilotindex')
            | {{ pilot.JDL_ID.match(/^J/) ? pilot.name : "-" }}
    hr
    .buttons
      button.btn.btn-lg.btn-success(type='button', v-on:click='start') スタート音 <kbd>1</kbd>
      nuxt-link.btn.btn-lg.btn-secondary(role='button', :to='prev()') 前のヒート<kbd>2</kbd>
      nuxt-link.btn.btn-lg.btn-primary(role='button', :to='next()') 次のヒート<kbd>3</kbd>
    #progress.progress(style={height: '30px'})
      .progress-bar(v-bind:style="{width: progress + '%'}") {{ currentTime }}
</template>

<script>
export default {
  asyncData ({ params }) {
    return { currentHeat: params.id }
  },
  data () {
    return {
      timer: -1,
      currentHeat: 1,
      progress: 0,
      currentTime: ''
    }
  },
  fetch ({ store, params, $axios }) {
    store.dispatch('initRaces')
    $axios.get('/api/' + params.id)
  },
  computed: {
    heats () {
      const total = this.$store.state.heats.length
      if (total === 0) { return }

      const current = this.currentHeat | 0
      const heats = []
      for (let i = current - 2; i <= current; i++) {
        const index = (i + total) % total
        const pilots = this.$store.state.heats[index]
        const klass = pilots.find(p => p.name).class
        heats.push({ index: index + 1, class: klass, pilots, active: i + 1 === current })
      }
      return heats
    }
  },
  beforeMount () {
    window.addEventListener('keydown', this.onKeyDown)
  },
  beforeDestroy () {
    this.stop()
    window.removeEventListener('keydown', this.onKeyDown)
  },
  methods: {
    start () {
      this.stop()
      this.$axios.get('/api/start')
      const startTime = Date.now()
      this.timer = setInterval(() => {
        const t = (Date.now() - startTime) / 1000
        const duration = 165
        const p = Math.min(t / duration * 100, 100)
        if (p === 100) {
          this.stop()
          this.goNext()
        }
        this.progress = p
        this.currentTime = `${Math.round(t)} / ${duration - Math.round(t)}`
      }, 100)
    },
    stop () {
      clearInterval(this.timer)
    },
    next () {
      const total = this.$store.state.heats.length
      if (total === 0) { return '' }
      const current = this.currentHeat | 0
      return `/${current === total ? 1 : current + 1}`
    },
    goNext () {
      this.$router.push(this.next())
    },
    prev () {
      const total = this.$store.state.heats.length
      if (total === 0) { return '' }
      const current = this.currentHeat | 0
      return `/${current === 1 ? total : current - 1}`
    },
    goPrevious () {
      this.$router.push(this.prev())
    },
    onKeyDown (event) {
      switch (event.key) {
        case '1':
          this.start()
          break
        case '2':
          this.goPrevious()
          break
        case '3':
          this.goNext()
          break
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
table
  font-size larger
th, td
  text-align center
tr.active
  font-size larger
  font-weight bold
.buttons
  text-align center
  a, button
    margin: 0 10px
#progress
  margin-top 15px
  .progress-bar
    font-size larger
</style>
