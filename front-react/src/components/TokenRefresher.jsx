import axios from 'axios';
import { useEffect } from 'react';
import Cookies from "js-cookie";
import { API_ENDPOINT } from '../shared/server';
import { useDispatch } from 'react-redux';
import { getUserIdAction } from '../redux/modules/registerActions';

export default function TokenRefresher({ children }) {
    const dispatch = useDispatch();
    const token = Cookies.get("access");

    useEffect(() => {
        dispatch(getUserIdAction(token));

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
                console.log('토큰이 성공적으로 갱신되었습니다.');
            } catch (error) {
                console.error('토큰 갱신 중 오류 발생:', error);
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
    }, [dispatch, token]);

    return <>{children}</>;
}
