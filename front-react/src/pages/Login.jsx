import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Link, useNavigate } from 'react-router-dom';
import IdPwForm from '../components/IdPwForm';
import axios from 'axios';
import { API_ENDPOINT } from '../shared/server';
import { useCookies } from 'react-cookie';

function Login() {
    const [cookies, setCookie, removeCookie] = useCookies(['access', 'refresh']);

    const navigate = useNavigate();

    const [id, setId] = useState('');
    const [pw, setPw] = useState('');

    const idHandler = (event) => {
        setId(event.target.value);
    };
    const pwHandler = (event) => {
        setPw(event.target.value);
    };

    const loginAction = async (data) => {
        const response = await axios.post(API_ENDPOINT + '/khis/account/login/', data);
        return response.data;
    };


    const onSubmit = async (event) => {
        event.preventDefault();
        const body = {
            username: id,
            password: pw,
        };

        try {
            const response = await loginAction(body);
            console.log(response);

            if (response.access) {
                setCookie('access', response.access, { path: '/', maxAge: 3600 }); // 쿠키에 액세스 토큰 저장
                setCookie('refresh', response.refresh, { path: '/', maxAge: 86400 }); // 쿠키에 리프레시 토큰 저장
                // console.log("쿠키 : ", cookies.get('refresh'))
                navigate('/');
            } else {
                alert('로그인 실패');
            }
        } catch (error) {
            console.error('로그인 에러:', error);
            alert('로그인 중 오류가 발생했습니다.');
        }
    };


    return (
        <Form className="d-flex flex-column align-items-center" onSubmit={onSubmit}>
            <IdPwForm id={id} pw={pw} idHandler={idHandler} pwHandler={pwHandler} />
            <div className="mt-3">
                <Button variant="primary" type="submit" className="mr-2">
                    로그인
                </Button>
                <Link to="/register/patient">
                    <Button variant="primary">회원가입</Button>
                </Link>
            </div>
        </Form>
    );
}

export default Login;
