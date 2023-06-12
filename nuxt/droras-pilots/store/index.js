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
  SET_TITLE (state, title) {
    state.title = title
  },
  ...vuexfireMutations
}
const db = firebase.firestore()
const currentRef = db.collection('race').doc('current')

export const state = () => ({
  title: '',
  current: { heat: 0 },
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
  async initTitle ({ commit, state }) {
    const cachedTitle = localStorage.getItem('title')
    if (cachedTitle) {
      commit('SET_TITLE', cachedTitle)
    }
    try {
      const response = await axios.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vQSIb1_Hys9ai97Mlf9LnxHaSFdWciZ2IC9kCTMbEQAHe7lvuM-7D-_8iKOtwibWMFL1ff1bP-keLJm/pub?gid=0&single=true&output=csv', { timeout: 10000 })
      const title = response.data.split(',')[1].trim()
      localStorage.setItem('title', title)
      commit('SET_TITLE', title)
    } catch (error) {
      console.error('Failed to fetch the title: ', error)
    }
  },
  async initRaces ({ commit, state }) {
    if (state.heats.length > 0) { return }

    const cachedHeats = JSON.parse(localStorage.getItem('heats')) || []
    if (cachedHeats.length > 0) {
      commit('SET_HEATS', cachedHeats)
    }

    try {
      const response = await axios.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vQSIb1_Hys9ai97Mlf9LnxHaSFdWciZ2IC9kCTMbEQAHe7lvuM-7D-_8iKOtwibWMFL1ff1bP-keLJm/pub?gid=554938252&single=true&output=csv', { timeout: 10000 })
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

      const filteredHeats = heats.filter(g => !!g)
      localStorage.setItem('heats', JSON.stringify(filteredHeats))
      commit('SET_HEATS', filteredHeats)
    } catch (error) {
      console.error('Failed to fetch the heats: ', error)
    }
  },
  initCurrent: firestoreAction(({
    bindFirestoreRef
  }) => {
    bindFirestoreRef('current', currentRef)
  })
}
