import instance from "./apis";

// 의료진이 연차 신청하는 API
export const postAnnual = async (data) => {
    const response = await instance.post(`/khis/schedule/medical/`, data);
    return response.data;
}

// 시작날짜, 종료날짜로 연차 조회 API
export const getAnnual = async (data) => {
    const response = await instance.get(`/khis/schedule/medical/specific/`, { params: { start_date: data.start_date, end_date: data.end_date } });
    return response.data;
}