import axios from 'axios';
import { useEffect } from 'react';
import Cookies from "js-cookie";
import { API_ENDPOINT } from '../apis/server';
import { useDispatch, useSelector } from 'react-redux';
import { getAccountInfoAction, getUserIdAction } from '../redux/modules/userActions';

export default function TokenRefresher({ children }) {
    const userId = useSelector(state => state.userReducer.userId);
    const dispatch = useDispatch();

    useEffect(() => {
        const token = Cookies.get("access");
        if (token) {
            console.log("userId", userId)
            dispatch(getUserIdAction(token));
            console.log("afteruserId", userId)
        }

        const refreshAPI = axios.create({
            baseURL: API_ENDPOINT,
            headers: { "Content-type": "application/json" },
        });

        const refreshAuthToken = async () => {
            try {
                const response = await refreshAPI.post('/khis/account/token/refresh/', {
                    refresh: Cookies.get('refresh'),
                });
                Cookies.set('access', response.data.access, { path: '' });
                console.log('토큰 갱신');
            } catch (error) {
                console.error('토큰 갱신 중 오류', error);
                Cookies.remove('access');
                Cookies.remove('refresh');
            }
        };

        refreshAPI.interceptors.response.use(
            response => response,
            async error => {
                const status = error.response?.status;
                if (status === 401 && Cookies.get('refresh')) {
                    await refreshAuthToken();
                }
                return Promise.reject(error);
            }
        );

        if (userId) {
            dispatch(getAccountInfoAction(userId));
        }
    }, [dispatch, userId]);

    return <>{children}</>;
}
