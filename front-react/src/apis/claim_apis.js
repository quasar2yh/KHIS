import instance from "./apis";

export const postClaim = async (data) => {
    const response = await instance.post('/khis/acceptance/claim/patient/', data);
    return response.data;
} 

export const getClaim = async (patientId) => {
    const response = await instance.get(`/khis/acceptance/claim/patient/${patientId}/`);
    return response.data;
}

export const postChargeItem = async (data) => {
    const response = await instance.post('/khis/acceptance/charge-item/', data);
    return response.data;
}