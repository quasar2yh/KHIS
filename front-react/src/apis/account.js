import axios from "axios";
import { API_ENDPOINT } from "../shared/server";

export const login = async (username, password) => {
    const response = await axios.post(API_ENDPOINT+'/khis/account/login/', { username, password });
    return response.data;
};

export const logout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
};

export  const singinPatient = async (username, password, name, telecom, subject, marital_status) => {
    const response = await axios.post(API_ENDPOINT + '/khis/account/register', {username, password, name, telecom, subject, marital_status});
    return response.data;
}