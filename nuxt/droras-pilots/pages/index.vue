<template>
  <div class="container">
    <div class="header">
      <div class="title">
        <img src="/jdl.png">
        <span>{{ title }}</span>
      </div>
      <table class="table freq">
        <thead>
          <tr>
            <th />
            <th>E1 / 5705</th>
            <th>F1 / 5740</th>
            <th>F4 / 5800</th>
          </tr>
        </thead>
      </table>
    </div>
    <table v-for="(klass, index) of heats" :key="index" class="table">
      <tbody class="list">
        <tr>
          <th colspan="4" class="class-name">
            {{ klass.class }}
          </th>
        </tr>
        <tr
          v-for="heat in klass.heats"
          :key="heat.index"
          :class="{ 'table-success': heat.active }"
        >
          <td><span class="index">{{ heat.index }}</span></td>
          <td v-for="(pilot, pilotindex) in heat.pilots" :key="pilotindex">
            {{ pilot.JDL_ID.match(/^J/) ? pilot.name : "-" }}
          </td>
        </tr>
      </tbody>
    </table>

    <div class="footer">
      <div>
        <a href="https://www.japandroneleague.com" target="new">JDL Official Web</a> |
        <a href="https://speedhive.mylaps.com/ja/Organizations/354884" target="new">MYLAPS Result</a> |
        <a href="https://www.japandroneleague.com/%E5%95%8F%E3%81%84%E5%90%88%E3%82%8F%E3%81%9B" target="new">Contact</a>
      </div>
      <div>©2023 JAPAN DRONE LEAGUE</div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    title () {
      return this.$store.state.title
    },
    heats () {
      const current = this.$store.state.current ? this.$store.state.current.heat | 0 : 0
      const allHeats = {}
      for (const [index, pilots] of this.$store.state.heats.entries()) {
        const pilot = pilots.find(p => p.name)
        const klass = pilot ? pilot.class : pilots[0].class
        if (!(klass in allHeats)) {
          allHeats[klass] = []
        }
        allHeats[klass].push({ index: index + 1, active: index + 1 === current, pilots })
      }
      return Object.entries(allHeats).map(([k, v]) => ({ class: k, heats: v }))
    }
  },
  created () {
    this.$store.dispatch('initTitle')
    this.$store.dispatch('initRaces')
    this.$store.dispatch('initCurrent')
  }
}
</script>

<style lang="stylus">
body
  background-color #111
</style>
<style lang="stylus" scoped>
.container
  position relative
  padding 0
  font-family 'BIZ UDPGothic', sans-serif
  font-size 16px
  font-weight 400
  color white
.container:before
  content ''
  display block
  position fixed
  top 0
  left 0
  z-index -1
  width 100%
  height 100vh
  background-image url('/bg3.jpg')
  background-size cover
  background-position: center

.header
  z-index 100
  position sticky
  top 0
  backdrop-filter blur(5px)
  img
    height 20px
    vertical-align middle
  .title
    text-align center
    font-weight: bold
    background-color #111
    padding 1vw 0
    border-bottom 1px solid #666
  .location
    font-weight 400
    font-size 0.8rem
  .freq
    font-size 0.7rem
    margin-bottom 0
    th
      border none
      background-color rgba(0, 0, 0, 0.4)
      color white

.table
  margin-bottom 40px

th, td
  text-align: center
  color: white
  border-color: #666
th
  backdrop-filter: blur(5px)
  background-color: rgba(255, 255, 255, 0.9)
  color: black
  font-weight: 700
  position: sticky
  top: 65px

.header th, .list td
  &:nth-child(1)
    width: 10%
    vertical-align: middle
  &:nth-child(2)
    width: 30%
  &:nth-child(3)
    width: 30%
  &:nth-child(4)
    width: 30%

.list .index
  // background-color rgba(255, 255, 255, 0.9)
  // color black
  border 1px solid white
  width 20px
  height 20px
  display flex
  align-items: center
  justify-content: center
  border-radius: 5px;
  font-size 0.7rem
  font-weight: 700

.table-success
  background-color: rgba(0, 128, 255, 0.4)
  > td, > th
      background-color: transparent
  font-weight: bold
  td
    color: #fff
    & .index
      background-color rgba(255, 255, 255, 0.9)
      color black
      border none

.class-name
  font-weight: bold
  font-size: smaller
  padding: 4px

.footer
  position: sticky
  bottom: 0
  width: 100%
  padding: 4px
  background-color rgba(0, 0, 0, 0.5)
  color: white
  text-align: center
  font-size: 0.6rem
  line-height: 1.7em
  backdrop-filter blur(5px)
  a
    color: #08f

</style>
