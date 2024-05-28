import { getAccountInfo, getUserId, getPatientInfo } from '../../apis/apis';

export const getUserIdAction = (token) => {
    const userId = getUserId(token);
    return {
        type: 'SET_USER_ID',
        payload: userId
    };
};

export const getPatientInfoAction = (patientId) => {
    const patientInfo = getPatientInfo(patientId);
    return {
        type: 'SET_PATIENT_INFO',
        payload: patientInfo
    };
};

export const getAccountInfoAction = (userId) => {
    const userAccountInfo = getAccountInfo(userId);
    return {
        type: 'SET_ACCOUNT_INFO',
        payload: userAccountInfo
    }
}
