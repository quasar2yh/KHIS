import axios from 'axios';
import { API_ENDPOINT } from '../../shared/server';

export const registerAction = (data) => async (dispatch) => {
    const response = await axios.post(API_ENDPOINT + '/khis/account/register/', data);
    dispatch({ type: 'SIGNUP', payload: response.data });
    return response.data;
};

export const loginAction = (data) => async (dispatch) => {
    const response = await axios.post(API_ENDPOINT + '/khis/account/login/', data);
    dispatch({ type: 'LOGIN', payload: response.data });
    return response.data;
};
