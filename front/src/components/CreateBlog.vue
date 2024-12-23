<template>
  <div class="create-blog bg-white p-6 rounded-lg shadow-sm">
    <h2 class="text-2xl font-semibold mb-6 text-gray-800">Create New Blog</h2>

    <div v-if="error" class="mb-4 p-4 bg-red-50 text-red-600 rounded-md">
      {{ error }}
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-6">
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

      <div class="flex justify-end">
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { blogApi } from '../services/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const error = ref(null)
const loading = ref(false)
const categories = ref([])

const formData = ref({
  title: '',
  content: '',
  category_id: '',
  tags: ''
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

    const tags = formData.value.tags
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag)

    const blogData = {
      title: formData.value.title,
      content: formData.value.content,
      category_id: formData.value.category_id || null,
      tags: tags,
      is_active: true
    }

    const response = await blogApi.createBlog(blogData)
    router.push(`/blogs/${response.id}`)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchCategories)
</script>

<style scoped>
.create-blog {
  max-width: 800px;
  margin: 2rem auto;
}
</style>
