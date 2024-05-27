import axios from 'axios';
import { useEffect } from 'react';
import { API_ENDPOINT } from '../shared/server';

export default function TokenRefresher({ children }) {
    useEffect(() => {
        const refreshAPI = axios.create({
            baseURL: API_ENDPOINT,
            headers: { "Content-type": "application/json" },
        })

        refreshAPI.interceptors.response.use(function (response) {
            // 2xx 범위에 있는 상태 코드는 이 함수를 트리거 합니다.
            // 응답 데이터가 있는 작업 수행
            return response;
        }, function (error) {
            // 2xx 외의 범위에 있는 상태 코드는 이 함수를 트리거 합니다.
            // 응답 오류가 있는 작업 수행
            const status = error.response.satus;
            console.log(status)
            return Promise.reject(error);
        });

    }, [])

    return <>{children}</>;
}
