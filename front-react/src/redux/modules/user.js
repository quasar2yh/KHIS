const initialState = {
    userId: null,
    patientInfo: null,
    practitionerInfo: null,
    AccountInfo: null,
};

const userReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'SET_USER_ID':
            return {
                ...state,
                userId: action.payload,
            };
        case 'SET_PATIENT_INFO':
            return {
                ...state,
                patientInfo: action.payload,
            };
        case 'SET_PRACTITIONER_INFO':
            return {
                ...state,
                practitionerInfo: action.payload,
            }
        case 'SET_ACCOUNT_INFO':
            return {
                ...state,
                AccountInfo: action.payload,
            };
        case 'RESET_USER':
            return {
                ...state,
                userId: action.payload,
                AccountInfo: action.payload
            }
        default:
            return state;
    }
};


export default userReducer;
