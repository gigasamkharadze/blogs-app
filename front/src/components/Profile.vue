<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
    <Navigation />
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div v-if="loading" class="text-center py-10">
          <svg class="animate-spin h-10 w-10 text-blue-600 mx-auto" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>

        <div v-else-if="error" class="text-center py-10">
          <p class="text-red-600">{{ error }}</p>
          <button
            @click="fetchProfile"
            class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-500"
          >
            Try Again
          </button>
        </div>

        <div v-else class="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
          <div class="p-8">
            <div class="flex flex-col md:flex-row items-start gap-8">
              <div class="w-full md:w-1/3">
                <div class="relative group">
                  <img
                    :src="profileImage"
                    alt="Profile"
                    class="w-full h-64 object-cover rounded-lg shadow-md"
                  >
                  <div
                    @click="triggerImageUpload"
                    class="absolute inset-0 bg-black bg-opacity-50 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-lg flex items-center justify-center cursor-pointer"
                  >
                    <span class="text-white text-sm font-medium">Change Photo</span>
                  </div>
                  <input
                    ref="imageInput"
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="handleImageChange"
                  >
                </div>
              </div>

              <div class="flex-1">
                <h1 class="text-2xl font-bold text-gray-900 mb-6">Profile Settings</h1>
                <form @submit.prevent="handleSubmit" class="space-y-6">
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        First Name
                      </label>
                      <input
                        v-model="form.first_name"
                        type="text"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                    </div>

                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        Last Name
                      </label>
                      <input
                        v-model="form.last_name"
                        type="text"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                    </div>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Email
                    </label>
                    <input
                      v-model="form.email"
                      type="email"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Username
                    </label>
                    <input
                      :value="username"
                      type="text"
                      readonly
                      class="w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-md"
                    >
                  </div>

                  <div v-if="successMessage" class="text-green-600 text-sm">
                    {{ successMessage }}
                  </div>

                  <div class="flex justify-end">
                    <button
                      type="submit"
                      class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-500 disabled:opacity-50"
                      :disabled="loading"
                    >
                      Save Changes
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { authApi } from '../services/api'
import Navigation from './Navigation.vue'
import { config } from './../config.js'
import { useAuthStore } from '../stores/auth'

const loading = ref(false)
const error = ref(null)
const successMessage = ref('')
const imageInput = ref(null)
const authStore = useAuthStore()

const username = computed(() => authStore.user?.username)

const form = ref({
  email: '',
  first_name: '',
  last_name: '',
  profile_image: null
})

const profileImage = computed(() => {
  if (!form.value.profile_image) return '/default-profile.png'
  if (form.value.profile_image.startsWith('http')) return form.value.profile_image
  return `${config.BACKEND_URL}${form.value.profile_image}`
})

const fetchProfile = async () => {
  loading.value = true
  error.value = null
  try {
    const profile = await authApi.getProfile()
    form.value = {
      email: profile.email || '',
      first_name: profile.first_name || '',
      last_name: profile.last_name || '',
      profile_image: profile.profile_image || null
    }
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  loading.value = true
  successMessage.value = ''
  error.value = null
  try {
    await authApi.updateProfile(form.value)
    successMessage.value = 'Profile updated successfully'
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const handleImageChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  loading.value = true
  error.value = null
  try {
    const response = await authApi.updateProfileImage(file)
    await fetchProfile()
    successMessage.value = 'Profile image updated successfully'
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
    if (imageInput.value) {
      imageInput.value.value = ''
    }
  }
}

const triggerImageUpload = () => {
  imageInput.value.click()
}

onMounted(fetchProfile)
</script>
