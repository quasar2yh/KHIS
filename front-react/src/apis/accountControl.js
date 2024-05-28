import axios from "axios";
import { API_ENDPOINT } from "../shared/server";
import Cookies from "js-cookie";
import base64 from 'base-64';

const instance = axios.create({
    baseURL: API_ENDPOINT,
    headers: { "Content-type": "application/json" },
});

// 인터셉터를 사용하여 요청에 토큰을 추가
instance.interceptors.request.use(
    config => {
        const token = Cookies.get("access");
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// access 토큰을 디코딩해서 user.id 얻기
export const getUserId = (token) => {
    try {
        const payload = token.substring(token.indexOf('.') + 1, token.lastIndexOf('.'));
        const decodingInfo = base64.decode(payload);
        const decodingInfoJson = JSON.parse(decodingInfo);
        return decodingInfoJson.user_id;
    } catch (error) {
        return null;
    }
}

export const registerAction = async (data) => {
    const response = await instance.post(API_ENDPOINT + '/khis/account/register/', data);
    return response.data;
}

export const loginAction = async (data) => {
    const response = await instance.post(API_ENDPOINT + '/khis/account/login/', data);
    return response.data;
};

export const appointmentAction = async (data, userId) => {
    const response = await instance.post(`/khis/appointment/patient/${userId}/`, data);
    return response.data;
};

export const getDepartments = async () => {
    const response = await instance.get(`/khis/schedule/department/`);
    return response.data;
};

export default instance;