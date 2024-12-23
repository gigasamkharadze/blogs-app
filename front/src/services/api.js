import { cookies } from '../utils/cookies'
import { config } from '../config'
import router from '../router'

const API_URL = config.API_URL

const handleUnauthorized = () => {
  cookies.remove('access_token')
  router.push('/login')
}

export const authApi = {
  async login(username, password) {
    const response = await fetch(`${API_URL}/users/token`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    })

    const data = await response.json()

    if (!response.ok) {
      if (data.detail?.includes('No User matches')) {
        throw new Error('Invalid username or password')
      }
      throw new Error(data.detail || 'Invalid credentials')
    }

    return data
  },

  async register(userData) {
    const response = await fetch(`${API_URL}/users/register`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    })

    const data = await response.json()

    if (!response.ok) {
      if (typeof data === 'object') {
        const cleanMessage = data.message ? data.message.replace('message: ', '') :
          Object.entries(data)
            .map(([field, messages]) => {
              const message = Array.isArray(messages) ? messages.join(', ') : messages
              return `${field}: ${message}`
            })
            .join('\n')
        throw new Error(cleanMessage)
      }
      throw new Error(data.detail || 'Registration failed')
    }

    return data
  },

  async getProfile() {
    try {
      const response = await fetch(`${API_URL}/users/profile`, {
        headers: {
          'Accept': 'application/json',
          'Authorization': `Bearer ${cookies.get('access_token')}`
        }
      })

      const responseText = await response.text()
      console.log('Raw API Response:', responseText)

      let data
      try {
        data = JSON.parse(responseText)
      } catch (e) {
        console.error('Failed to parse JSON:', e)
        throw new Error('Invalid response from server')
      }

      if (!response.ok) {
        if (response.status === 401) {
          handleUnauthorized()
        }
        throw new Error(data.detail || 'Failed to fetch profile')
      }

      return data
    } catch (error) {
      console.error('Profile fetch error:', error)
      throw error
    }
  },

  async updateProfile(profileData) {
    try {
      const response = await fetch(`${API_URL}/users/profile`, {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${cookies.get('access_token')}`
        },
        body: JSON.stringify({
          email: profileData.email,
          first_name: profileData.first_name,
          last_name: profileData.last_name
        })
      })

      const responseText = await response.text()
      console.log('Update Profile Response:', responseText)

      let data
      try {
        data = JSON.parse(responseText)
      } catch (e) {
        console.error('Failed to parse JSON:', e)
        throw new Error('Invalid response from server')
      }

      if (!response.ok) {
        if (response.status === 401) {
          handleUnauthorized()
        }
        throw new Error(data.detail || 'Failed to update profile')
      }

      return data
    } catch (error) {
      console.error('Profile update error:', error)
      throw error
    }
  },

  async updateProfileImage(imageFile) {
    try {
      const formData = new FormData()
      formData.append('file', imageFile)

      const response = await fetch(`${API_URL}/users/profile/image`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${cookies.get('access_token')}`
        },
        body: formData
      })

      const responseText = await response.text()
      console.log('Update Image Response:', responseText)

      let data
      try {
        data = JSON.parse(responseText)
      } catch (e) {
        console.error('Failed to parse JSON:', e)
        throw new Error('Invalid response from server')
      }

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to update profile image')
      }

      return data
    } catch (error) {
      console.error('Profile image update error:', error)
      throw error
    }
  },

  async getCategories() {
    try {
      const response = await fetch(`${API_URL}/blogs/categories`, {
        headers: {
          'Accept': 'application/json',
          'Authorization': `Bearer ${cookies.get('access_token')}`
        }
      })

      const responseText = await response.text()
      console.log('Categories Response:', responseText)

      let data
      try {
        data = JSON.parse(responseText)
      } catch (e) {
        console.error('Failed to parse categories JSON:', e)
        throw new Error('Invalid response from server')
      }

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to fetch categories')
      }

      return data
    } catch (error) {
      console.error('Categories fetch error:', error)
      throw error
    }
  }
}

export const blogApi = {
  async getBlogs({
                   page = 1,
                   pageSize = 10,
                   dateFrom = '',
                   dateTo = '',
                   ordering = '-created_at'
                 } = {}) {
    const params = new URLSearchParams({
      page,
      page_size: pageSize,
      ordering
    })

    if (dateFrom) {
      const fromDate = new Date(dateFrom)
      params.append('date_from', fromDate.toISOString().split('T')[0])
    }
    if (dateTo) {
      const toDate = new Date(dateTo)
      params.append('date_to', toDate.toISOString().split('T')[0])
    }

    const response = await fetch(`${API_URL}/blogs/?${params}`, {
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${cookies.get('access_token')}`
      }
    })

    const data = await response.json()

    if (!response.ok) {
      if (response.status === 401) {
        handleUnauthorized()
      }
      throw new Error(data.detail || 'Failed to fetch blogs')
    }

    return data
  },

  async getBlogById(id) {
    try {
      const response = await fetch(`${API_URL}/blogs/${id}`, {
        headers: {
          'Accept': 'application/json',
          'Authorization': `Bearer ${cookies.get('access_token')}`
        }
      })

      if (!response.ok) {
        if (response.status === 401) {
          handleUnauthorized()
        }
        if (response.status === 404) {
          throw new Error('Blog not found')
        }
        const errorData = await response.text()
        console.error('API Error Response:', errorData)
        throw new Error('Failed to fetch blog')
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  },

  async updateBlog(id, blogData) {
    try {
      const formData = new FormData()

      // Add all fields to FormData
      if (blogData.title !== undefined) {
        formData.append('title', blogData.title)
      }
      if (blogData.content !== undefined) {
        formData.append('content', blogData.content)
      }
      if (blogData.category_id !== undefined) {
        formData.append('category_id', blogData.category_id)
      }
      if (blogData.tags !== undefined) {
        formData.append('tags', JSON.stringify(blogData.tags))
      }
      if (blogData.is_active !== undefined) {
        formData.append('is_active', blogData.is_active)
      }
      if (blogData.image) {
        formData.append('image', blogData.image)
      }

      const response = await fetch(`${API_URL}/blogs/${id}`, {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Authorization': `Bearer ${cookies.get('access_token')}`
        },
        body: formData
      })

      if (!response.ok) {
        if (response.status === 401) {
          handleUnauthorized()
        }
        const errorData = await response.text()
        throw new Error(errorData || 'Failed to update blog')
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('Update blog error:', error)
      throw error
    }
  },

  async deleteBlog(id) {
    const response = await fetch(`${API_URL}/blogs/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${cookies.get('access_token')}`
      }
    })

    if (!response.ok) {
      if (response.status === 401) {
        handleUnauthorized()
      }
      const data = await response.json()
      throw new Error(data.detail || 'Failed to delete blog')
    }
  },

  async getComments(blogId) {
    try {
      const response = await fetch(`${API_URL}/blogs/${blogId}/comments/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${cookies.get('access_token')}`
        }
      })

      if (!response.ok) {
        if (response.status === 401) {
          handleUnauthorized()
        }
        const errorData = await response.text()
        throw new Error('Failed to fetch comments')
      }

      const data = await response.json()
      console.log('Raw API response:', data)
      return data
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  },

  async addComment(blogId, content) {
    const response = await fetch(`${API_URL}/blogs/${blogId}/comments/`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${cookies.get('access_token')}`
      },
      body: JSON.stringify({ content })
    })

    const data = await response.json()
    if (!response.ok) {
      if (response.status === 401) {
        handleUnauthorized()
      }
      throw new Error(data.detail || 'Failed to add comment')
    }
    return data
  },

  async updateComment(blogId, commentId, content) {
    const response = await fetch(`${API_URL}/blogs/${blogId}/comments/${commentId}/`, {
      method: 'PUT',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${cookies.get('access_token')}`
      },
      body: JSON.stringify({ content })
    })

    const data = await response.json()
    if (!response.ok) {
      if (response.status === 401) {
        handleUnauthorized()
      }
      throw new Error(data.detail || 'Failed to update comment')
    }
    return data
  },

  async deleteComment(blogId, commentId) {
    const response = await fetch(`${API_URL}/blogs/${blogId}/comments/${commentId}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${cookies.get('access_token')}`
      }
    })

    if (!response.ok) {
      if (response.status === 401) {
        handleUnauthorized()
      }
      const data = await response.json()
      throw new Error(data.detail || 'Failed to delete comment')
    }
  },

  async likeComment(blogId, commentId) {
    const response = await fetch(`${API_URL}/blogs/${blogId}/comments/${commentId}/like/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${cookies.get('access_token')}`
      }
    })

    if (!response.ok) {
      if (response.status === 401) {
        handleUnauthorized()
      }
      const data = await response.json()
      throw new Error(data.detail || 'Failed to like comment')
    }
  },

  async dislikeComment(blogId, commentId) {
    const response = await fetch(`${API_URL}/blogs/${blogId}/comments/${commentId}/dislike/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${cookies.get('access_token')}`
      }
    })

    if (!response.ok) {
      if (response.status === 401) {
        handleUnauthorized()
      }
      const data = await response.json()
      throw new Error(data.detail || 'Failed to dislike comment')
    }
  },

  getCategories: async () => {
    const response = await fetch(`${API_URL}/blogs/categories`, {
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${cookies.get('access_token')}`
      }
    })

    if (!response.ok) {
      if (response.status === 401) {
        handleUnauthorized()
      }
      const data = await response.json()
      throw new Error(data.detail || 'Failed to fetch categories')
    }

    return await response.json()
  },

  async createBlog(blogData) {
    try {
      const formData = new FormData()

      // Add the image first if it exists
      if (blogData.image) {
        formData.append('image', blogData.image)
      }

      // Remove image from blogData before converting to JSON
      const { image, ...blogDataWithoutImage } = blogData

      // Convert blog data to JSON string
      formData.append('blog', JSON.stringify(blogDataWithoutImage))

      const response = await fetch(`${API_URL}/blogs/`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Authorization': `Bearer ${cookies.get('access_token')}`
        },
        body: formData
      })

      const data = await response.json()
      console.log('Create blog response:', data)

      if (!response.ok) {
        if (response.status === 401) {
          handleUnauthorized()
        }

        if (response.status === 422 && data.detail) {
          if (Array.isArray(data.detail)) {
            throw new Error(data.detail.map(err =>
              `${err.loc[err.loc.length - 1]}: ${err.msg}`
            ).join('\n'))
          }
          throw new Error(typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail))
        }

        throw new Error(data.detail || 'Failed to create blog')
      }

      return data
    } catch (error) {
      console.error('Create blog error:', error)
      throw error
    }
  }
}
