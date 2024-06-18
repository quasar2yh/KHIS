import axios from "axios";
import Cookies from "js-cookie";
import base64 from 'base-64';

const API_ENDPOINT = 'http://127.0.0.1:8000'

const instance = axios.create({
    baseURL: API_ENDPOINT,
    headers: { "Content-type": "application/json" },
    withCredentials: true,
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

instance.interceptors.response.use(

    // response가 정상이면 response 리턴
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        const status = error.response?.status;

        // response error 401(권한 문제)면 refreshAuthToken 함수 실행
        if (status === 401) {
            try {
                await refreshAuthToken();
                return instance(originalRequest);
            } catch (error) {
                console.error('토큰 갱신 실패:', error);
                return Promise.reject(error);
            }
        }
        return Promise.reject(error);
    }
);

// 토큰 갱신 함수
async function refreshAuthToken() {
    try {
        const response = await instance.post('/khis/account/token/refresh/');
        Cookies.set('access', response.data.access);
    } catch (error) {
        console.error('토큰 갱신 에러:', error);
        Cookies.remove('access');
        logoutAction();
        throw error;
    }
}

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

// 회원가입 API
export const registerAction = async (data) => {
    const response = await instance.post('/khis/account/register/', data);
    return response.data;
}

// 로그인 API
export const loginAction = async (data) => {
    const response = await instance.post('/khis/account/login/', data);
    return response.data;
};

export const logoutAction = async () => {
    const response = await instance.post('/khis/account/logout/');
    return response.data;
};

// usrId로 계정 정보 가져오는 API
export const getAccountInfo = async (userId) => {
    if (userId) {
        const response = await instance.get(`/khis/account/${userId}/`);
        return response.data;
    }
    else {
        return null;
    }
};

// 비밀번호 변경 API
export const passwordChange = async (userId, data) => {
    const response = await instance.put(`/khis/account/pwchange/${userId}/`, data);
    return response.data;
}

// 부서 조회 API
export const getDepartments = async () => {
    const response = await instance.get(`/khis/schedule/department/`);
    return response.data;
};

// 환자 정보 조회 API
export const getPatientInfo = async (patientId) => {
    const response = await instance.get(`/khis/patient-registration/${patientId}/`);
    return response.data;
};

// 환자 정보 수정 API(프로필 수정)
export const updatePatientInfo = async (patientId, data) => {
    const response = await instance.put(`/khis/patient-registration/${patientId}/`, data);
    return response.data;
}

// 의료진 정보 조회 API
export const getPractitionerInfo = async (practitionerId) => {
    const response = await instance.get(`/khis/practitioner-registration/${practitionerId}/`);
    return response.data;
};

// 의료진 정보 수정 API(프로필 수정)
export const updatePractitionerInfo = async (practitionerId, data) => {
    const response = await instance.put(`/khis/practitioner-registration/${practitionerId}/`, data);
    return response.data;
};

// 환자를 이름이나 연락처로 검색하는 API
export const searchPatient = async ({ name, telecom }) => {
    const response = await instance.get('/khis/patient-registration/search/', { params: { name, telecom } });
    return response.data;
}

// ChatGPT API
export const sendChatMessage = async (data) => {
    const response = await instance.post(`/khis/appointment/chatbot/`, data);
    return response.data;
}

// 병원 휴일 조회 
export const getHoliday = async () => {
    const response = await instance.get(`/khis/schedule/hospital/public/`)
    return response.data;
}

// 부서별 의사 조회
export const getPractitionerFromDepartment = async (departmentId) => {
    const response = await instance.get(`/khis/schedule/department/${departmentId}/practitioner/`)
    return response.data;
}

export const getMedicalRecord = async (patientId) => {
    const response = await instance.get(`/khis/consultations/${patientId}/`)
    return response.data;
}


// 환자 대기열 조회
export const getWaitingList = async () => {
    const response = await instance.get(`/khis/appointment/waiting/`);
    return response.data;
};

//전체 유저 조회 
export const getAllUser = async ()=>{
    const response = await instance.get('khis/account/alluser/')
    return response.data;
}
//메세지 조회
export const getChatMessages = async ()=>{
    const response = await instance.get('/khis/chat/messages/')
    return response.data;
}
//메세지 보내기
export const sendMessage = async (receiver, message) => {
    const response = await instance.post('/khis/chat/messages/', {
      receiver,
      message,
    });
    return response.data;
  };
export default instance;