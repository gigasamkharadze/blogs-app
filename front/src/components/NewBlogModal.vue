<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-2xl">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-semibold text-gray-800">Create New Blog</h2>
        <button @click="onClose" class="text-gray-500 hover:text-gray-700">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div v-if="error" class="mb-4 p-4 bg-red-50 text-red-600 rounded-md whitespace-pre-line">
        {{ error }}
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700">Title</label>
          <input
            id="title"
            v-model="formData.title"
            type="text"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div>
          <label for="category" class="block text-sm font-medium text-gray-700">Category</label>
          <div class="relative mt-1">
            <select
              id="category"
              v-model="formData.category_id"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select a category</option>
              <template v-if="categories.length">
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.title }}
                </option>
                <template v-for="category in categories" :key="category.id">
                  <option
                    v-for="child in category.children"
                    :key="child.id"
                    :value="child.id"
                  >
                    ↳ {{ child.title }}
                  </option>
                </template>
              </template>
            </select>
          </div>
        </div>

        <div>
          <label for="content" class="block text-sm font-medium text-gray-700">Content</label>
          <textarea
            id="content"
            v-model="formData.content"
            rows="6"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          ></textarea>
        </div>

        <div>
          <label for="tags" class="block text-sm font-medium text-gray-700">
            Tags (comma separated)
          </label>
          <input
            id="tags"
            v-model="formData.tags"
            type="text"
            placeholder="tag1, tag2, tag3"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div>
          <label for="image" class="block text-sm font-medium text-gray-700">
            Image
          </label>
          <input
            id="image"
            type="file"
            @change="handleImageChange"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div class="flex justify-end gap-3 mt-6">
          <button
            type="button"
            @click="onClose"
            class="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? 'Creating...' : 'Create Blog' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { blogApi } from '../services/api'

const props = defineProps({
  onClose: {
    type: Function,
    required: true
  },
  onBlogCreated: {
    type: Function,
    required: true
  }
})

const error = ref(null)
const loading = ref(false)
const categories = ref([])

const formData = ref({
  title: '',
  content: '',
  category_id: '',
  tags: '',
  image: null
})

const fetchCategories = async () => {
  try {
    const response = await blogApi.getCategories()
    categories.value = response.results || []
  } catch (err) {
    error.value = err.message
  }
}

const handleSubmit = async () => {
  try {
    loading.value = true
    error.value = null

    if (!formData.value.category_id) {
      error.value = 'Please select a category'
      return
    }

    const tags = formData.value.tags
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag)

    const blogData = {
      title: formData.value.title,
      content: formData.value.content,
      category_id: parseInt(formData.value.category_id),
      tags: tags,
      is_active: true,
      image: formData.value.image
    }

    const response = await blogApi.createBlog(blogData)
    props.onBlogCreated(response)
    props.onClose()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    formData.value.image = file
  }
}

onMounted(fetchCategories)
</script>
