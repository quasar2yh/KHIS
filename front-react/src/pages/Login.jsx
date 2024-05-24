import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Link, useNavigate } from 'react-router-dom';
import IdPwForm from '../components/IdPwForm';
import { login } from '../apis/account';

function Login() {
    const [id, setId] = useState('');
    const [pw, setPw] = useState('');

    const idHandler = (event) => {
        setId(event.target.value);
    };
    const pwHandler = (event) => {
        setPw(event.target.value);
    };

    const router = useNavigate();
    const onSubmit = async (event) => {
        event.preventDefault(); // 새로고침 시 폼 제출 동작 방지
        try {
            const result = await login(id, pw); // apis/login

            const { access, refresh } = result; // result를 구조 분해 할당 
            localStorage.setItem('access', access);
            localStorage.setItem('refresh', refresh);
            router('/') // Home으로 리렌더링
        } catch (error) {
            console.error('로그인 실패:', error);
        }
    };

    return (
        <Form className="d-flex flex-column align-items-center" onSubmit={onSubmit}>
            <IdPwForm id={id} pw={pw} idHandler={idHandler} pwHandler={pwHandler} />
            <div className="mt-3">
                <Button variant="primary" type="submit" className="mr-2">
                    로그인
                </Button>
                <Link to="/signin/patient">
                    <Button variant="primary">회원가입</Button>
                </Link>
            </div>
        </Form>
    );
}

export default Login;
