import axios from "axios";
import { API_ENDPOINT } from "../shared/server";

export const registerAction = async (data) => {
    const response = await axios.post(API_ENDPOINT + '/khis/account/register/', data);
    return response.data;
}

export const loginAction = async (data) => {
    const response = await axios.post(API_ENDPOINT + '/khis/account/login/', data);
    return response.data;
};
