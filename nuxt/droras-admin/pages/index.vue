<template>
  <div class="container">
    <table class="table">
      <thead>
        <tr>
          <th></th>
          <th>E1: 5705</th>
          <th>F1: 5740</th>
          <th>F4: 5800</th>
        </tr>
      </thead>
      <tbody id="list">
        <tr
          v-for="(heat, index) in heats"
          :key="index"
          v-bind:class="{ 'table-success': index == currentHeat }"
        >
          <td>{{ index }}</td>
          <td
            v-for="(pilot, index) in heat"
            :key="index"
          >{{ pilot.JDL_ID.match(/^J/) ? pilot.name : '-' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      heats: [],
      currentHeat: 0
    }
  },
  created() {
    setInterval(async () => {
      const current = await this.$axios.$get(
        'http://localhost:8080/api/get_cur_heat'
      )
      console.log(current)
      this.currentHeat = current.id
    }, 3000)
  },
  async asyncData({ app }) {
    const heats = await app.$axios.$get(
      'http://localhost:8080/api/get_race_data'
    )
    const current = await app.$axios.$get(
      'http://localhost:8080/api/get_cur_heat'
    )
    // console.log(heats)
    return { heats: heats, currentHeat: current.id }
  },
  methods: {
    async getCurrent() {
      this.currentHeat++
    }
  }
}
</script>

<style　scoped>
</style>
