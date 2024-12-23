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
            @click="fetchBlog"
            class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-500"
          >
            Try Again
          </button>
        </div>

        <div v-else-if="blog" class="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
          <div class="relative">
            <img
              v-if="blog.image"
              :src="getImageUrl(blog.image)"
              :alt="blog.title"
              class="w-full max-h-[600px] object-contain bg-gray-100"
            >
          </div>

          <div class="p-6">
            <div class="flex justify-between items-start mb-4">
              <h1 class="text-3xl font-bold text-gray-900">{{ blog.title }}</h1>
              <div v-if="isOwner" class="flex space-x-2">
                <button
                  @click="showEditModal = true"
                  class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-500 flex items-center"
                >
                  <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  Edit
                </button>
                <button
                  @click="handleDelete"
                  class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-500 flex items-center"
                >
                  <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Delete
                </button>
              </div>
            </div>
            <div class="flex items-center text-gray-500 mb-6">
              <span class="mr-4">By {{ blog.author }}</span>
              <span>{{ formatDateTime(blog.created_at) }}</span>
            </div>
            <div v-if="blog.tags && blog.tags.length > 0" class="flex flex-wrap gap-2 mb-6">
              <span
                v-for="tag in blog.tags"
                :key="tag"
                class="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-sm border border-blue-100"
              >
                {{ tag }}
              </span>
            </div>
            <div class="prose max-w-none" v-html="blog.content"></div>
          </div>

          <div class="border-t border-gray-200 p-6">
            <h3 class="text-xl font-bold mb-4">Comments</h3>

            <form @submit.prevent="handleAddComment" class="mb-6">
              <div class="mb-4">
                <label class="block text-gray-700 text-sm font-bold mb-2">
                  Add a comment
                </label>
                <textarea
                  v-model="newComment"
                  rows="3"
                  required
                  placeholder="Write your comment here..."
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ></textarea>
              </div>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-500"
              >
                Post Comment
              </button>
            </form>

            <Comments
              ref="commentsRef"
              :blogId="route.params.id"
              :isOwner="isOwner"
            />
          </div>
        </div>
      </div>
    </div>

    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full">
        <h2 class="text-2xl font-bold mb-4">Edit Blog</h2>
        <form @submit.prevent="handleSave">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">
              Title
            </label>
            <input
              v-model="editForm.title"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">
              Content
            </label>
            <textarea
              v-model="editForm.content"
              rows="6"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            ></textarea>
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">
              Category ID
            </label>
            <input
              v-model="editForm.category_id"
              type="number"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">
              Tags (comma separated)
            </label>
            <input
              v-model="editForm.tags"
              type="text"
              placeholder="tag1, tag2, tag3"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">
              Image
            </label>
            <input
              type="file"
              accept="image/*"
              @change="handleImageChange"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>
          <div class="flex justify-end space-x-2">
            <button
              type="button"
              @click="showEditModal = false"
              class="px-4 py-2 text-gray-600 hover:text-gray-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-500"
            >
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import {computed, onMounted, ref} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {authApi, blogApi} from '../services/api'
import {useAuthStore} from '../stores/auth'
import Navigation from './Navigation.vue'
import Comments from './Comments.vue'

export default {
  name: 'BlogDetail',
  components: {
    Navigation,
    Comments
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const blog = ref(null)
    const currentUser = ref(null)
    const loading = ref(true)
    const error = ref(null)
    const showEditModal = ref(false)
    const newComment = ref('')
    const editForm = ref({
      title: '',
      content: '',
      category_id: null,
      tags: '',
      image: null
    })

    const authStore = useAuthStore()

    const isOwner = computed(() => {
      const isOwnerResult = blog.value && currentUser.value && blog.value.author === currentUser.value.username
      return isOwnerResult
    })

    const getImageUrl = (imagePath) => {
      if (!imagePath) return ''
      if (imagePath.startsWith('http')) return imagePath
      return `http://127.0.0.1:8000${imagePath}`
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

    const fetchBlog = async () => {
      try {
        loading.value = true
        error.value = null
        blog.value = await blogApi.getBlogById(route.params.id)
        editForm.value = {
          title: blog.value.title,
          content: blog.value.content,
          category_id: blog.value.category?.id || null,
          tags: blog.value.tags.join(', '),
          image: null
        }
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const fetchCurrentUser = async () => {
      try {
        const response = await authApi.getProfile()
        currentUser.value = response
        authStore.setUser(response)
      } catch (error) {
        console.error('Error fetching current user:', error)
      }
    }

    const handleSave = async () => {
      try {
        loading.value = true

        const tagsArray = editForm.value.tags.split(',').map(tag => tag.trim()).filter(tag => tag)

        const blogData = {
          title: editForm.value.title,
          content: editForm.value.content,
          category_id: editForm.value.category_id,
          tags: tagsArray,
          is_active: blog.value.is_active,
          image: editForm.value.image
        }

        blog.value = await blogApi.updateBlog(route.params.id, blogData)
        showEditModal.value = false
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const handleImageChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        editForm.value.image = file
      }
    }

    const handleDelete = async () => {
      if (!confirm('Are you sure you want to delete this blog?')) return

      try {
        loading.value = true
        await blogApi.deleteBlog(route.params.id)
        await router.push('/')
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const commentsRef = ref(null)

    const handleAddComment = async () => {
      if (!newComment.value.trim()) {
        error.value = 'Comment cannot be empty'
        return
      }

      try {
        const response = await blogApi.addComment(route.params.id, newComment.value.trim())
        newComment.value = ''
        if (commentsRef.value) {
          await commentsRef.value.fetchComments()
        }
      } catch (err) {
        console.error('Error adding comment:', err)
        error.value = 'Failed to add comment'
      }
    }

    onMounted(async () => {
      try {
        await fetchCurrentUser()
        await fetchBlog()
      } catch (error) {
        console.error('Error initializing component:', error)
      }
    })

    return {
      blog,
      loading,
      error,
      isOwner,
      showEditModal,
      editForm,
      newComment,
      route,
      formatDateTime,
      handleSave,
      handleDelete,
      getImageUrl,
      handleImageChange,
      handleAddComment,
      commentsRef
    }
  }
}
</script>

<style scoped>
.blog-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.blog-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.blog-meta {
  color: #666;
  margin: 10px 0;
  display: flex;
  gap: 20px;
}

.blog-image {
  max-width: 100%;
  height: auto;
  margin: 20px 0;
  border-radius: 4px;
}

.blog-text {
  line-height: 1.6;
  margin-top: 20px;
}

.tags {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.tag {
  background: #f0f0f0;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
  color: #666;
}
</style>
