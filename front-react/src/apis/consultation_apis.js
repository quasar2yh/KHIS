import instance from "./apis";

// 환자 본인의 진료기록 조회 API
export const getConsultations = async (patientId) => {
    const response = await instance.get(`/khis/consultations/${patientId}/`);
    return response.data;
}

// 의료진이 진료기록 생성하는 API
export const postConsultation = async (data) => {
    const response = await instance.post(`/khis/consultations/`, data);
    return response.data;
}

