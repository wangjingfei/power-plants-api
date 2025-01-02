import axios from 'axios';

const api = axios.create({
    baseURL: 'https://api.wjf.me',
    withCredentials: true,  // 如果需要发送认证信息
    headers: {
        'Content-Type': 'application/json'
    }
});

export default api; 