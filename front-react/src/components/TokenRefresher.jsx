import axios from 'axios';
import { useEffect } from 'react';
import { useCookies } from 'react-cookie';
import { API_ENDPOINT } from '../shared/server';

export default function TokenRefresher({ children }) {
    const [cookies, setCookie, removeCookie] = useCookies(['access', 'refresh']);

    useEffect(() => {
        const refreshAPI = axios.create({
            baseURL: API_ENDPOINT,
            headers: { "Content-type": "application/json" },
        });

        const refreshAuthToken = async () => {
            try {
                const response = await refreshAPI.post('/khis/account/token/refresh/', {
                    refresh: cookies.refresh_token,
                });
                setCookie('access', response.data.access, { path: '/', maxAge: 3600 });
                console.log('토큰이 성공적으로 갱신되었습니다.');
            } catch (error) {
                console.error('토큰 갱신 중 오류 발생:', error);
                removeCookie('access');
                removeCookie('refresh');
                // 필요한 경우 로그인 페이지로 리디렉션 또는 다른 처리
            }
        };

        refreshAPI.interceptors.response.use(
            function (response) {
                // 2xx 범위에 있는 상태 코드는 이 함수를 트리거 합니다.
                // 응답 데이터가 있는 작업 수행
                return response;
            },
            function (error) {
                // 2xx 외의 범위에 있는 상태 코드는 이 함수를 트리거 합니다.
                // 응답 오류가 있는 작업 수행
                const status = error.response?.status;
                if (status === 401 && cookies.refresh_token) {
                    // 401 에러가 발생하고, 리프레시 토큰이 있으면 토큰 갱신 시도
                    refreshAuthToken();
                }
                return Promise.reject(error);
            }
        );

        if (cookies.refresh_token) {
            // 컴포넌트가 마운트될 때 리프레시 토큰이 있으면 갱신 시도
            refreshAuthToken();
        }
    }, [cookies, setCookie, removeCookie]);

    return <>{children}</>;
}
