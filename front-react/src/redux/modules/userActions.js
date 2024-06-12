import { getAccountInfo, getUserId, getPatientInfo, getPractitionerInfo } from '../../apis/apis';

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

export const getPractitionerInfoAction = (prectitionerId) => {
    const practitionerInfo = getPractitionerInfo(prectitionerId);
    return {
        type: 'SET_PRACTITIONER_INFO',
        payload: practitionerInfo
    };
};

export const getAccountInfoAction = (userId) => {
    const accountInfo = getAccountInfo(userId);
    return {
        type: 'SET_ACCOUNT_INFO',
        payload: accountInfo
    }
};

export const resetUserAction = () => ({
    type: 'RESET_USER',
});