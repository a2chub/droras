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
      button#btn-start.btn.btn-lg.btn-success(type='button', v-on:click='start') スタート音 <kbd>1</kbd>
      nuxt-link#btn-prev.btn.btn-lg.btn-secondary(role='button', :to='prev') 前のヒート<kbd>2</kbd>
      nuxt-link#btn-next.btn.btn-lg.btn-primary(role='button', :to='next') 次のヒート<kbd>3</kbd>
    #progress.progress(style={height: '30px'})
      .progress-bar(v-bind:style="{width: progress + '%'}") {{ current }}
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      timer: -1,
      progress: 0,
      current: ''
    }
  },
  validate ({ params }) {
    return /^\d+$/.test(params.id)
  },
  computed: {
    heats () {
      const total = this.$store.state.heats.length
      if (total === 0 || !this.$store.state.current) { return }

      const current = this.$store.state.current.heat | 0
      const heats = []
      for (let i = current - 2; i <= current; i++) {
        const index = (i + total) % total
        const pilots = this.$store.state.heats[index]
        const klass = pilots.find(p => p.name).class
        heats.push({ index: index + 1, class: klass, pilots, active: i + 1 === current })
      }
      return heats
    },
    next () {
      const total = this.$store.state.heats.length
      if (total === 0 || !this.$store.state.current) { return '' }

      const current = this.$store.state.current.heat | 0
      return `/${current === total ? 1 : current + 1}`
    },
    prev () {
      const total = this.$store.state.heats.length
      if (total === 0 || !this.$store.state.current) { return '' }

      const current = this.$store.state.current.heat | 0
      return `/${current === 1 ? total : current - 1}`
    }
  },
  async fetch ({ store, params, $axios }) {
    await store.dispatch('initRaces')
    await store.dispatch('initCurrent')
    await axios.get('/api/' + params.id)
  },
  beforeDestroy () {
    this.stop()
  },
  methods: {
    start () {
      this.$axios.get('/api/start')
      const startTime = Date.now()
      this.timer = setInterval(() => {
        const t = (Date.now() - startTime) / 1000
        const duration = 120
        const p = Math.min(t / duration * 100, 100)
        if (p === 100) {
          this.stop()
        }
        this.progress = p
        this.current = `${Math.round(t)} / ${duration - Math.round(t)}`
      }, 100)
    },
    stop () {
      clearInterval(this.timer)
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