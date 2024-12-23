import { defineStore } from 'pinia'
import { authApi } from '../services/api'
import { cookies } from '../utils/cookies'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: cookies.get('access_token'),
    user: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(username, password) {
      try {
        const data = await authApi.login(username, password)
        this.token = data.access_token
        cookies.set('access_token', data.access_token)

        const profile = await authApi.getProfile()
        this.user = profile

        return true
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },

    logout() {
      this.token = null
      this.user = null
      cookies.remove('access_token')
    },

    setUser(user) {
      this.user = user
    }
  }
})
