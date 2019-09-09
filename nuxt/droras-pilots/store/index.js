import {
  vuexfireMutations,
  firestoreAction
} from 'vuexfire'
import axios from 'axios'
import firebase from '@/plugins/firebase'

export const mutations = {
  SET_HEATS (state, heats) {
    state.heats = heats
  },
  ...vuexfireMutations
}
const db = firebase.firestore()
const currentRef = db.collection('race').doc('current')

export const state = () => ({
  current: {},
  heats: []
})

export const getters = {
  current: (state) => {
    return state.current
  },
  heats: (state) => {
    return state.heats
  }
}

export const actions = {
  async initRaces ({ commit }) {
    const response = await axios.get('https://script.google.com/macros/s/AKfycbwY05MtkIet6Yc_MlQvD9Ng4H_ZTpBcFZvtTj_BPE008Az8H8x2/exec?getrace=6')
    const heats = []
    for (const data of response.data) {
      const [JDL_ID, name, klass, index] = data
      let group = heats[index]
      if (!group) {
        group = []
        heats[index] = group
      }
      group.push({
        JDL_ID,
        name,
        'class': klass,
        'heat': index
      })
    }
    commit('SET_HEATS', heats.filter(g => !!g))
  },
  initCurrent: firestoreAction(({
    bindFirestoreRef
  }) => {
    bindFirestoreRef('current', currentRef)
  })
}
