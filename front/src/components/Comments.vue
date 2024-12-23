<template>
  <div class="comments-section bg-white p-6 rounded-lg shadow-sm">
    <h3 class="text-2xl font-semibold mb-6 text-gray-800">Comments</h3>

    <div v-if="loading" class="flex items-center justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <div v-else-if="error" class="bg-red-50 text-red-600 p-4 rounded-md mb-4">
      {{ error }}
    </div>

    <div v-else>
      <div v-if="comments && comments.length > 0" class="space-y-4">
        <div v-for="comment in comments" :key="comment.id" class="comment">
          <div class="comment-main">
            <div class="comment-header flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
                <div class="comment-author font-medium text-gray-700">{{ comment.author }}</div>
              </div>
              <div v-if="isCommentAuthor(comment)" class="flex items-center gap-2">
                <button
                  v-if="!isEditing(comment.id)"
                  @click="startEditing(comment)"
                  class="text-gray-500 hover:text-blue-600"
                >
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                </button>
              </div>
            </div>
            <div v-if="isEditing(comment.id)" class="mb-2">
              <textarea
                v-model="editContent"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows="3"
              ></textarea>
              <div class="flex justify-end gap-2 mt-2">
                <button
                  @click="cancelEdit"
                  class="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
                >
                  Cancel
                </button>
                <button
                  @click="saveEdit(comment)"
                  class="px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-500"
                >
                  Save
                </button>
              </div>
            </div>
            <div v-else class="comment-content">{{ comment.content }}</div>

            <div class="flex items-center gap-4 mt-3">
              <button
                @click="handleLike(comment)"
                class="flex items-center gap-1 text-gray-500 hover:text-blue-600"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                </svg>
                <span>{{ comment.likes || 0 }}</span>
              </button>
              <button
                @click="handleDislike(comment)"
                class="flex items-center gap-1 text-gray-500 hover:text-red-600"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018c.163 0 .326.02.485.06L17 4m-7 10v5a2 2 0 002 2h.095c.5 0 .905-.405.905-.905 0-.714.211-1.412.608-2.006L17 13V4m-7 10h2m5 0h2a2 2 0 002-2v-6a2 2 0 00-2-2h-2.5" />
                </svg>
                <span>{{ comment.dislikes || 0 }}</span>
              </button>
              <button
                @click="startReplying(comment)"
                class="flex items-center gap-1 text-gray-500 hover:text-blue-600"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
                </svg>
                <span>Reply</span>
              </button>
            </div>

            <div v-if="isReplying(comment.id)" class="mt-4 pl-4 border-l-2 border-blue-200">
              <textarea
                v-model="replyContent"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows="3"
                placeholder="Write your reply..."
              ></textarea>
              <div class="flex justify-end gap-2 mt-2">
                <button
                  @click="cancelReply"
                  class="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
                >
                  Cancel
                </button>
                <button
                  @click="submitReply(comment)"
                  class="px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-500"
                >
                  Submit Reply
                </button>
              </div>
            </div>
          </div>

          <div v-if="comment.children && comment.children.length > 0" class="nested-comments">
            <div v-for="child in comment.children" :key="child.id" class="comment">
              <div class="comment-main">
                <div class="comment-header flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <div class="comment-author font-medium text-gray-700">{{ child.author }}</div>
                  </div>
                  <!-- Edit button for child comment author -->
                  <div v-if="isCommentAuthor(child)" class="flex items-center gap-2">
                    <button
                      v-if="!isEditing(child.id)"
                      @click="startEditing(child)"
                      class="text-gray-500 hover:text-blue-600"
                    >
                      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                      </svg>
                    </button>
                  </div>
                </div>
                <div v-if="isEditing(child.id)" class="mb-2">
                  <textarea
                    v-model="editContent"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows="3"
                  ></textarea>
                  <div class="flex justify-end gap-2 mt-2">
                    <button
                      @click="cancelEdit"
                      class="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
                    >
                      Cancel
                    </button>
                    <button
                      @click="saveEdit(child)"
                      class="px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-500"
                    >
                      Save
                    </button>
                  </div>
                </div>
                <div v-else class="comment-content">{{ child.content }}</div>

                <div class="flex items-center gap-4 mt-3">
                  <button
                    @click="handleLike(child)"
                    class="flex items-center gap-1 text-gray-500 hover:text-blue-600"
                  >
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                    </svg>
                    <span>{{ child.likes || 0 }}</span>
                  </button>
                  <button
                    @click="handleDislike(child)"
                    class="flex items-center gap-1 text-gray-500 hover:text-red-600"
                  >
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018c.163 0 .326.02.485.06L17 4m-7 10v5a2 2 0 002 2h.095c.5 0 .905-.405.905-.905 0-.714.211-1.412.608-2.006L17 13V4m-7 10h2m5 0h2a2 2 0 002-2v-6a2 2 0 00-2-2h-2.5" />
                    </svg>
                    <span>{{ child.dislikes || 0 }}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-8 text-gray-500">
        <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
        <p class="text-gray-600">No comments yet. Be the first to comment!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineExpose } from 'vue'
import { blogApi } from '../services/api'
import { useAuthStore } from '../stores/auth'

const props = defineProps({
  blogId: {
    type: [String, Number],
    required: true
  },
  isOwner: {
    type: Boolean,
    default: false
  }
})

const authStore = useAuthStore()
const comments = ref([])
const loading = ref(true)
const error = ref(null)
const editingCommentId = ref(null)
const editContent = ref('')
const replyingToId = ref(null)
const replyContent = ref('')

const fetchComments = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await blogApi.getComments(props.blogId)
    comments.value = response.results || []
  } catch (err) {
    console.error('Error fetching comments:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const isCommentAuthor = (comment) => {
  return authStore.user?.username === comment.author
}

const isEditing = (commentId) => {
  return editingCommentId.value === commentId
}

const startEditing = (comment) => {
  editingCommentId.value = comment.id
  editContent.value = comment.content
}

const cancelEdit = () => {
  editingCommentId.value = null
  editContent.value = ''
}

const saveEdit = async (comment) => {
  try {
    await blogApi.updateComment(props.blogId, comment.id, editContent.value)
    await fetchComments()
    cancelEdit()
  } catch (err) {
    error.value = err.message
  }
}

const handleLike = async (comment) => {
  try {
    const commentToUpdate = comments.value.find(c => c.id === comment.id) ||
      comments.value.flatMap(c => c.children).find(child => child.id === comment.id)

    if (commentToUpdate) {
      commentToUpdate.likes += 1
    }

    await blogApi.likeComment(props.blogId, comment.id)
  } catch (err) {
    if (commentToUpdate) {
      commentToUpdate.likes -= 1
    }
    error.value = err.message
  }
}

const handleDislike = async (comment) => {
  try {
    const commentToUpdate = comments.value.find(c => c.id === comment.id) ||
      comments.value.flatMap(c => c.children).find(child => child.id === comment.id)

    if (commentToUpdate) {
      commentToUpdate.dislikes += 1
    }

    await blogApi.dislikeComment(props.blogId, comment.id)
  } catch (err) {
    if (commentToUpdate) {
      commentToUpdate.dislikes -= 1
    }
    error.value = err.message
  }
}

const isReplying = (commentId) => {
  return replyingToId.value === commentId
}

const startReplying = (comment) => {
  replyingToId.value = comment.id
  replyContent.value = ''
}

const cancelReply = () => {
  replyingToId.value = null
  replyContent.value = ''
}

const submitReply = async (parentComment) => {
  if (!replyContent.value.trim()) {
    error.value = 'Reply cannot be empty'
    return
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/blogs/${props.blogId}/comments/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify({
        content: replyContent.value.trim(),
        parent_id: parentComment.id
      })
    })

    if (response.ok) {
      cancelReply()
      await fetchComments()
    } else {
      const errorData = await response.json()
      error.value = errorData.message || 'Failed to add reply'
    }
  } catch (err) {
    console.error('Error adding reply:', err)
    error.value = 'Failed to add reply'
  }
}

onMounted(fetchComments)

defineExpose({
  fetchComments
})
</script>

<style scoped>
.comments-section {
  margin-top: 1rem;
  border: 1px solid #e5e7eb;
}

.comment {
  padding: 1.25rem;
  margin-bottom: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  background-color: white;
  transition: all 0.2s;
}

.comment:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.comment-main {
  display: flex;
  flex-direction: column;
}

.comment-content {
  color: #4b5563;
  font-size: 1rem;
  line-height: 1.5;
  white-space: pre-wrap;
}

.nested-comments {
  margin-top: 1rem;
  margin-left: 2rem;
  padding-left: 1rem;
  border-left: 2px solid #e5e7eb;
}

.nested-comments .comment {
  background-color: #f9fafb;
}

@media (max-width: 640px) {
  .nested-comments {
    margin-left: 1rem;
  }
}
</style>
