<template>
  <div class="blog-comments">
    <h3 class="text-xl font-semibold mb-4">Comments</h3>

    <div v-if="loading" class="text-gray-500">
      Loading comments...
    </div>

    <div v-else-if="error" class="text-red-500">
      {{ error }}
    </div>

    <Comments v-else :comments="comments"  blog-id="props.blogId" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { blogApi } from '../services/api'
import Comments from './Comments.vue'

const props = defineProps({
  blogId: {
    type: [String, Number],
    required: true
  }
})

const comments = ref([])
const loading = ref(true)
const error = ref(null)

const fetchComments = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await blogApi.getComments(props.blogId)
    comments.value = response.results || []
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchComments)
</script>
