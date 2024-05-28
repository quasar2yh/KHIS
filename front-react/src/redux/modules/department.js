const initialState = {
    departmentList: null
};

const departmentReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'SET_DEPARTMENT_LIST':
            return {
                ...state,
                departmentList: action.payload,
            };
        default:
            return state;
    }
};

export default departmentReducer;
