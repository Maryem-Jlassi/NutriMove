import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000/users/',  // Ensure this matches your Django server
});

export const setAxiosInterceptors = (navigate, setError) => {
  axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;

      if (error.response && error.response.status === 401 && error.response.data.token_class === "AccessToken") {
        try {
          const refreshToken = localStorage.getItem('refresh_token');
          const response = await axios.post('http://127.0.0.1:8000/users/api/token/refresh/', { refresh: refreshToken });

          // Update tokens in localStorage and axios instance
          localStorage.setItem('token', response.data.access);
          axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;

          // Retry the original request with the new token
          originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
          return axiosInstance(originalRequest);
        } catch (refreshError) {
          console.error("Token refresh failed:", refreshError);
          setError("Session expired. Please log in again.");
          localStorage.clear();
          navigate('/login');  // Redirect to login if refresh fails
        }
      }
      return Promise.reject(error);
    }
  );
};

export default axiosInstance;
