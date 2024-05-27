const initialState = {
    user: null,
    isLogged: false,
};

const user = (state = initialState, action) => {
    switch (action.type) {
        case 'SIGNUP':
            return {
                ...state,
                user: action.payload,
            };
        default:
            return state;
    }
};


export default user;
