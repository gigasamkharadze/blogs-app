<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
    <Navigation />
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <div class="mb-6 flex justify-between items-center">
            <h2 class="text-2xl font-bold text-gray-900">Blogs</h2>
            <button
              v-if="isAuthenticated"
              @click="showNewBlogModal = true"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-500 flex items-center"
            >
              <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              New Blog
            </button>
          </div>

          <div class="mb-8 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <div class="flex flex-col space-y-4">
              <div class="flex justify-between items-center">
                <h1 class="text-2xl font-semibold text-blue-900">Blogs</h1>

                <button
                  v-if="hasActiveFilters"
                  @click="clearFilters"
                  class="px-4 py-2 text-sm text-blue-600 hover:text-blue-500 flex items-center space-x-2 transition-colors duration-200 border border-blue-200 rounded-md hover:border-blue-300 bg-white"
                >
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  <span>Clear Filters</span>
                </button>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="relative">
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Sort by
                  </label>
                  <div class="relative">
                    <select
                      v-model="filters.ordering"
                      class="block w-full pl-3 pr-10 py-2.5 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 rounded-lg shadow-sm transition-colors duration-200 bg-white appearance-none"
                    >
                      <option value="-created_at">Latest (Date & Time)</option>
                      <option value="created_at">Oldest (Date & Time)</option>
                    </select>
                    <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                      <svg
                        class="h-4 w-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Date From
                  </label>
                  <div class="relative">
                    <input
                      type="date"
                      v-model="filters.dateFrom"
                      @change="handleDateChange"
                      class="block w-full pl-3 pr-10 py-2.5 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 rounded-lg shadow-sm transition-colors duration-200 bg-white"
                    >
                    <div class="pointer-events-none absolute right-0 top-0 bottom-0 flex items-center px-2 text-gray-400">
                      <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Date To
                  </label>
                  <div class="relative">
                    <input
                      type="date"
                      v-model="filters.dateTo"
                      @change="handleDateChange"
                      class="block w-full pl-3 pr-10 py-2.5 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 rounded-lg shadow-sm transition-colors duration-200 bg-white"
                    >
                    <div class="pointer-events-none absolute right-0 top-0 bottom-0 flex items-center px-2 text-gray-400">
                      <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="loading" class="text-center py-10">
            <svg class="animate-spin h-10 w-10 text-blue-600 mx-auto" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>

          <div v-else-if="error" class="text-center py-10">
            <p class="text-red-600">{{ error }}</p>
            <button
              @click="fetchBlogs"
              class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-500 border border-blue-700"
            >
              Try Again
            </button>
          </div>

          <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <BlogCard
              v-for="blog in sortedBlogs"
              :key="blog.id"
              :blog="blog"
            />
          </div>

          <div v-if="blogs.length > 0" class="mt-6 flex justify-between items-center">
            <button
              v-if="previousPage"
              @click="currentPage--"
              class="px-4 py-2 text-sm bg-white text-blue-600 rounded-md hover:bg-blue-50 border border-blue-200 transition-colors duration-200"
            >
              Previous
            </button>
            <span class="text-gray-600">Page {{ currentPage }}</span>
            <button
              v-if="nextPage"
              @click="currentPage++"
              class="px-4 py-2 text-sm bg-white text-blue-600 rounded-md hover:bg-blue-50 border border-blue-200 transition-colors duration-200"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>

    <NewBlogModal
      v-if="showNewBlogModal"
      @close="showNewBlogModal = false"
      @blog-created="handleBlogCreated"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import Navigation from './Navigation.vue'
import BlogCard from './BlogCard.vue'
import NewBlogModal from './NewBlogModal.vue'
import { blogApi } from '../services/api'

const authStore = useAuthStore()
const blogs = ref([])
const loading = ref(false)
const error = ref(null)
const currentPage = ref(1)
const nextPage = ref(null)
const previousPage = ref(null)
const showNewBlogModal = ref(false)
const isAuthenticated = computed(() => authStore.isAuthenticated)

const filters = reactive({
  dateFrom: '',
  dateTo: '',
  ordering: '-created_at',
  pageSize: 10
})

const sortedBlogs = computed(() => {
  const sortedArray = [...blogs.value]

  sortedArray.sort((a, b) => {
    const dateA = new Date(a.created_at).getTime()
    const dateB = new Date(b.created_at).getTime()

    return filters.ordering === '-created_at'
      ? dateB - dateA
      : dateA - dateB
  })

  return sortedArray
})

const hasActiveFilters = computed(() => {
  return filters.dateFrom ||
         filters.dateTo ||
         filters.ordering !== '-created_at'
})

const handleDateChange = async () => {
  if (filters.dateFrom && filters.dateTo) {
    const fromDate = new Date(filters.dateFrom)
    const toDate = new Date(filters.dateTo)

    if (toDate < fromDate) {
      filters.dateTo = ''
      return
    }
  }

  currentPage.value = 1
  await fetchBlogs()
}

const fetchBlogs = async () => {
  try {
    loading.value = true
    error.value = null

    const dateFrom = filters.dateFrom ? new Date(filters.dateFrom).toISOString().split('T')[0] : ''
    const dateTo = filters.dateTo ? new Date(filters.dateTo).toISOString().split('T')[0] : ''

    const response = await blogApi.getBlogs({
      page: currentPage.value,
      pageSize: filters.pageSize,
      dateFrom,
      dateTo
    })

    blogs.value = response.results
    nextPage.value = response.next
    previousPage.value = response.previous
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filters.dateFrom = ''
  filters.dateTo = ''
  filters.ordering = '-created_at'
  currentPage.value = 1
  fetchBlogs()
}

const handleBlogCreated = async () => {
  showNewBlogModal.value = false
  await fetchBlogs()
}

fetchBlogs()
</script>

<style scoped>
select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  opacity: 0;
  position: absolute;
  right: 0;
  top: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}
</style>
