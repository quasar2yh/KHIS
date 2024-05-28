import axios from 'axios';
import { API_ENDPOINT } from '../../shared/server';
import { getUserId } from '../../apis/accountControl';

export const registerAction = (data) => async (dispatch) => {
    const response = await axios.post(API_ENDPOINT + '/khis/account/register/', data);
    dispatch({ type: 'SIGNUP', payload: response.data });
    return response.data;
};


export const getUserIdAction = (token) => {
    const userId = getUserId(token);
    return {
        type: 'SET_USER_ID',
        payload: userId
    };
};