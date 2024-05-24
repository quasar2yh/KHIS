import axios from "axios"
import { API_ENDPOINT } from "../shared/server"

export const getProfile = async () => {
    const access = localStorage.getItem('access');
    axios.get(API_ENDPOINT + '/profile', {
        headers: {
            Authorization: access,
        },
    });
    return result.data
}