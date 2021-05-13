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
  async initRaces ({ commit, state }) {
    if (state.heats.length > 0) { return }

    const response = await axios.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vQSIb1_Hys9ai97Mlf9LnxHaSFdWciZ2IC9kCTMbEQAHe7lvuM-7D-_8iKOtwibWMFL1ff1bP-keLJm/pub?gid=554938252&single=true&output=csv')
    const heats = []
    for (const data of response.data.split('\n')) {
      const [JDL_ID, name, klass, _index] = data.split(',')
      const index = parseInt(_index)
      let group = heats[index]
      if (!group) {
        group = []
        heats[index] = group
      }
      group.push({
        JDL_ID,
        name,
        class: klass,
        heat: index
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
