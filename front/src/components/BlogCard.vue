<template>
  <div
    @click="navigateToBlog"
    class="bg-white rounded-lg shadow-sm overflow-hidden border border-gray-200 hover:border-blue-300 transition-colors duration-200 cursor-pointer"
  >
    <img
      v-if="blog.image"
      :src="getImageUrl(blog.image)"
      :alt="blog.title"
      class="w-full h-48 object-cover border-b border-gray-200"
    >
    <div class="p-4">
      <h2 class="text-xl font-semibold text-blue-900">{{ blog.title }}</h2>
      <div class="mt-2 flex flex-wrap gap-2">
        <span
          v-for="tag in blog.tags"
          :key="tag"
          class="px-2 py-1 text-xs bg-blue-50 text-blue-600 rounded-full border border-blue-200"
        >
          {{ tag }}
        </span>
      </div>
      <div class="mt-4 flex justify-between items-center">
        <span class="text-sm text-blue-600">
          {{ formatDateTime(blog.created_at) }}
        </span>
        <span class="text-sm text-gray-500">
          By {{ blog.author }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { config } from './../config.js'

const router = useRouter()
const props = defineProps({
  blog: {
    type: Object,
    required: true
  }
})

const navigateToBlog = () => {
  router.push(`/blogs/${props.blog.id}`)
}

const getImageUrl = (imagePath) => {
  if (!imagePath) return ''
  if (imagePath.startsWith('http')) return imagePath
  return `${config.BACKEND_URL}${imagePath}`
}

const formatDateTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
