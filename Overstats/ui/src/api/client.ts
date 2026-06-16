import axios from 'axios'
import type { AxiosInstance } from 'axios'

const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '',
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
  },
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      return Promise.reject(new Error('Request timed out after 120 seconds'))
    }
    return Promise.reject(error)
  }
)

export default apiClient
