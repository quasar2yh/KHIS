import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Link, useNavigate } from 'react-router-dom';
import IdPwForm from '../components/IdPwForm';
import { loginAction } from '../apis/apis';
import Cookies from 'js-cookie';
import { useDispatch, useSelector } from 'react-redux';
import { getAccountInfoAction, getUserIdAction } from '../redux/modules/userActions';

function Login() {
    //userReducer의 userId
    const userId = useSelector(state => state.userReducer.userId);
    const dispatch = useDispatch()
    const navigate = useNavigate();
    const [id, setId] = useState('');
    const [pw, setPw] = useState('');

    const idHandler = (event) => {
        setId(event.target.value);
    };

    const pwHandler = (event) => {
        setPw(event.target.value);
    };

    // 로그인 버튼 누르면 실행되는 함수
    const onSubmit = async (event) => {
        event.preventDefault();

        // 서버가 받는 로그인 json 형식
        const body = {
            username: id,
            password: pw,
        };

        try {
            const response = await loginAction(body);

            // response에 access 토큰이 있다면 Cookie에 세팅
            if (response.access) {
                Cookies.set('access', response.access, { path: '' });
                Cookies.set('refresh', response.refresh, { path: '' }); 
            
                // access 토큰 디코딩 후 userId 반환하는 API
                dispatch(getUserIdAction(response.access));

                // userId로 AccountInfo 반환하는 API
                dispatch(getAccountInfoAction(userId));

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
