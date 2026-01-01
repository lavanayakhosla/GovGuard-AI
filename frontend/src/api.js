import axios from 'axios';      
export default axios.create({
  baseURL: 'http://localhost:8000', // Adjust the base URL as needed
});