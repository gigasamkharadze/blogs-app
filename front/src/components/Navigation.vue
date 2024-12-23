<template>
  <nav class="bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <router-link
            to="/"
            class="flex items-center px-2 py-2 text-xl font-bold text-blue-600 hover:text-blue-500 transition-colors duration-200"
          >
            Blog App
          </router-link>
        </div>

        <div class="flex items-center space-x-4">
          <template v-if="isAuthenticated">
            <!-- Profile Link with Icon -->
            <router-link
              to="/profile"
              class="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors duration-200"
            >
              <div class="relative w-8 h-8 rounded-full overflow-hidden bg-gray-200">
                <img
                  v-if="profileImage"
                  :src="getImageUrl(profileImage)"
                  alt="Profile"
                  class="w-full h-full object-cover"
                >
                <svg
                  v-else
                  class="w-full h-full text-gray-400 p-1"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
              </div>
              <span class="text-sm font-medium hidden md:block">{{ username }}</span>
            </router-link>

            <button
              @click="handleLogout"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Logout
            </button>
          </template>

          <template v-else>
            <router-link
              to="/login"
              class="px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-500"
            >
              Login
            </router-link>
            <router-link
              to="/register"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-500"
            >
              Register
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { authApi } from '../services/api'
import { config } from './../config.js'

const router = useRouter()
const authStore = useAuthStore()
const profileImage = ref(null)

const isAuthenticated = computed(() => authStore.isAuthenticated)
const username = computed(() => authStore.user?.username)

const getImageUrl = (imagePath) => {
  if (!imagePath) return ''
  if (imagePath.startsWith('http')) return imagePath
  return `${config.BACKEND_URL}${imagePath}`
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const fetchProfileImage = async () => {
  if (isAuthenticated.value) {
    try {
      const profile = await authApi.getProfile()
      profileImage.value = profile.profile_image
    } catch (error) {
      console.error('Failed to fetch profile image:', error)
    }
  }
}

onMounted(fetchProfileImage)

watch(() => isAuthenticated.value, (newValue) => {
  if (newValue) {
    fetchProfileImage()
  } else {
    profileImage.value = null
  }
})
</script>
