import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Link, useNavigate } from 'react-router-dom';
import IdPwForm from '../components/IdPwForm';
import { loginAction } from '../apis/accountControl';
import Cookies from 'js-cookie';

function Login() {

    const navigate = useNavigate();

    const [id, setId] = useState('');
    const [pw, setPw] = useState('');

    const idHandler = (event) => {
        setId(event.target.value);
    };
    const pwHandler = (event) => {
        setPw(event.target.value);
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
                Cookies.set('access', response.access, { path: ''}); // 쿠키에 액세스 토큰 저장
                Cookies.set('refresh', response.refresh, { path: ''}); // 쿠키에 리프레시 토큰 저장
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
                <Link to="/register">
                    <Button variant="primary">회원가입</Button>
                </Link>
            </div>
        </Form>
    );
}

export default Login;
