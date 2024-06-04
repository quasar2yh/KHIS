import axios from "axios";
import { API_ENDPOINT } from "./server";
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

// 인터셉터로 리스폰이 401이면 도중에 refresh
instance.interceptors.response.use(

    // response가 정상이면 response 리턴
    (response) => response,  
    async (error) => {          
        const originalRequest = error.config;
        const status = error.response?.status;

        // response error 401(권한 문제)면서 Cookie에 refresh 가 있다면
        // refreshAuthToken 함수 실행
        if (status === 401 && Cookies.get('refresh')) {
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
        // 쿠키에서 refresh 가져와서 token/refresh API로 토큰 갱신 요청
        const refresh = Cookies.get('refresh');
        const response = await instance.post('/khis/account/token/refresh/', { refresh });

        // 우리 서버는 access, refresh 둘 다 줘서 둘 다 새로 갱신
        Cookies.set('access', response.data.access);
        Cookies.set('refresh', response.data.refresh);
    } catch (error) {
        console.error('토큰 갱신 에러:', error);

        // 갱신 에러 시 쿠키에서 토큰 전부 제거
        Cookies.remove('access');
        Cookies.remove('refresh');
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
    const response = await instance.post(API_ENDPOINT + '/khis/account/register/', data);
    return response.data;
}

// 로그인 API
export const loginAction = async (data) => {
    const response = await instance.post(API_ENDPOINT + '/khis/account/login/', data);
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


// 환자가 진료 예약하는 API
export const postAppointment = async (data, userId) => {
    const response = await instance.post(`/khis/appointment/patient/${userId}/`, data);
    return response.data;
};


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

// 환자 본인의 예약 내역 조회 API
export const getAppointmentStatus = async (patientId) => {
    const response = await instance.get(`/khis/appointment/patient/${patientId}/`);
    return response.data;
};

// ChatGPT API
export const sendChatMessage = async (data) => {
    const response = await instance.post(`/khis/appointment/chatbot/`, data);
    return response.data;
}

// 환자 본인의 진료기록 조회 API
export const getConsultations = async (patientId) => {
    const response = await instance.get(`/khis/consultations/${patientId}/`);
    return response.data;
}

// 환자를 이름이나 연락처로 검색하는 API
export const searchPatient = async ({ name, telecom }) => {
    const response = await instance.get('/khis/patient-registration/search/', { params: { name, telecom } });
    return response.data;
}

// 의료진이 진료기록 생성하는 API
export const postConsultation = async (data) => {
    const response = await instance.post(`/khis/consultations/`, data);
    return response.data;
}

// 의료진이 연차 신청하는 API
export const annualAction = async (data) => {
    const response = await instance.post(`/khis/schedule/medical/`, data);
    return response.data;
}

// 시작날짜, 종료날짜로 연차 조회 API
export const getAnnual = async (data) => {
    const response = await instance.get(`/khis/schedule/medical/specific/`, { params: { start_date: data.start_date, end_date: data.end_date } });
    return response.data;
}

// 해당 부서, 날짜, 시간에 진료 가능한 의사 조회
export const getAbleAppointmentPractitioner = async ({ date, time, department }) => {
    const response = await instance.get(`/khis/appointment/checklist/`, { params: { date, time, department } });
    return response.data;
}

// 병원 휴일 조회 
export const getHoliday = async () => {
    const response = await instance.get(`/khis/schedule/hospital/Public/`)
    return response.data;
}

// 부서별 의사 조회
export const getPractitionerFromDepartment = async (departmentId) => { 
    const response = await instance.get(`/khis/schedule/department/${departmentId}/Practitioner/`)
    return response.data;
}

export const getMedicalRecord = async (patientId) => {
    const response = await instance.get(`/khis/consultations/${patientId}/`)
    return response.data;
}

export const postProcedureRecord = async (data) => {
    const response = await instance.post(`/khis/consultations/procedure-record/`, data)
    return response.data;
}

export const getProcedureRecordList = async (medicalRecordId) => {
    const response = await instance.get(`/khis/consultations/procedure-record-list/${medicalRecordId}/`)
    return response.data;
}

export default instance;