export const state = () => ({
  heats: [],
  current: 0
})

export const mutations = {
  setHeats (state, heats) {
    state.heats = heats
  },
  setCurrent (state, index) {
    state.current = index
  }
}

export const actions = {
  async nuxtServerInit ({
    commit
  }, {
    app
  }) {
    const heats = await app.$axios.$get('/api/heat-data')
    commit('setHeats', heats)
    const current = await app.$axios.$get('/api/current-heat')
    commit('setCurrent', current.id)
  }
}
