import axios from 'axios'

const backendapi = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  }
})

export default { backendapi }
