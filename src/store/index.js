import { createStore } from 'vuex'

export default createStore({
  state: {
    role:null
  },
  getters: {
  },
  mutations: {
    role(state,payload){
      state.role=payload
    }
  },
  actions: {
  },
  modules: {
  }
})
