<template>
  <div class="container">
    <table class="table">
      <thead>
        <tr>
          <th />
          <th>E1: 5705</th>
          <th>F1: 5740</th>
          <th>F4: 5800</th>
        </tr>
      </thead>
      <tbody v-for="(klass, index) of heats" :key="index" class="list">
        <tr>
          <td colspan="4" class="class-name">
            {{ klass.class }}
          </td>
        </tr>
        <tr
          v-for="heat in klass.heats"
          :key="heat.index"
          :class="{ 'table-success': heat.active }"
        >
          <td>{{ heat.index }}</td>
          <td v-for="(pilot, pilotindex) in heat.pilots" :key="pilotindex">
            {{ pilot.JDL_ID.match(/^J/) ? pilot.name : "-" }}
          </td>
        </tr>
      </tbody>
    </table>

    <div class="footer">
      <a href="https://www.japandroneleague.com" target="new">JDL HP</a> |
      <a href="https://speedhive.mylaps.com/ja/Organizations/354884" target="new">Lap Result</a> |
      <a href="https://www.japandroneleague.com/%E5%95%8F%E3%81%84%E5%90%88%E3%82%8F%E3%81%9B" target="new">Contact</a>
      <br>
      <p>© 2015 JAPAN DRONE LEAGUE</p>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    heats () {
      const current = this.$store.state.current.heat | 0
      const allHeats = { open: [], expert: [], pro: [] }
      for (const [index, pilots] of this.$store.state.heats.entries()) {
        const klass = pilots.find(p => p.name).class.toLowerCase()
        allHeats[klass].push({ index: index + 1, active: index + 1 === current, pilots })
      }
      return [
        { class: 'Open', heats: allHeats.open },
        { class: 'Expert', heats: allHeats.expert },
        { class: 'Pro', heats: allHeats.pro }
      ]
    }
  },
  created () {
    this.$store.dispatch('initRaces')
    this.$store.dispatch('initCurrent')
  }
}
</script>

<style scoped>
.container{
  padding-bottom: 65px;
}
th, td {
  text-align: center;
}

.class-name {
  font-weight: bold;
}

.footer{
  position: fixed;
  font-color: black;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 61px;
  background-color: #bbbbbb;
  color: white;
  text-align: center;
}
a:link { color: #0000ff; }
a:visited { color: #000080; }
a:hover { color: #ff0000; }
a:active { color: #ff8000; }
</style>
