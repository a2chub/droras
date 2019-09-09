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
      <tbody id="list">
        <tr
          v-for="(heat, index) in $store.state.heats"
          :key="index"
          :class="{ 'table-success': index + 1 == $store.state.current.heat }"
        >
          <td>{{ index + 1 }}</td>
          <td v-for="(pilot, pilotindex) in heat" :key="pilotindex">
            {{ pilot.JDL_ID.match(/^J/) ? pilot.name : "-" }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  created () {
    this.$store.dispatch('initRaces')
    this.$store.dispatch('initCurrent')
  }
}
</script>
