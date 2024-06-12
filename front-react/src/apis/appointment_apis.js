import instance from "./apis";

// 환자가 진료 예약하는 API
export const postAppointment = async (data, patientId) => {
    const response = await instance.post(`/khis/appointment/patient/${patientId}/`, data);
    return response.data;
};

export const deleteAppointment = async (data, appointmentId) => {
    const response = await instance.delete(`/api/appointments/patient/${appointmentId}/`, data);
    return response.data;
};

// 환자 본인의 예약 내역 조회 API
export const getAppointmentStatus = async (patientId) => {
    const response = await instance.get(`/khis/appointment/patient/${patientId}/`);
    return response.data;
};

// 해당 부서, 날짜, 시간에 진료 가능한 의사 조회
export const getAbleAppointmentPractitioner = async ({ date, time, department }) => {
    const response = await instance.get(`/khis/appointment/checklist/`, { params: { date, time, department } });
    return response.data;
}