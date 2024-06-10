import instance from "./apis";

export const postProcedureRecord = async (data) => {
    const response = await instance.post(`/khis/consultations/procedure-record/`, data)
    return response.data;
}

export const getProcedureRecordList = async (medicalRecordId) => {
    const response = await instance.get(`/khis/consultations/procedure-record-list/${medicalRecordId}/`)
    return response.data;
}

export const updateProcedureRecord = async (procedureRecordId, data) => {
    const response = await instance.put(`/khis/consultations/procedure-record/${procedureRecordId}/`, data)
    return response.data;
}

export const getProcedure = async (patientId) => {
    const response = await instance.get(`/khis/procedure/${patientId}/`)
    return response.data;
}

export const getUnchargedProcedure = async (patientId) => {
    const response = await instance.get(`/khis/procedure/uncharged/${patientId}/`)
    return response.data;
}