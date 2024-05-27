import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Link, useNavigate } from 'react-router-dom';
import IdPwForm from '../components/IdPwForm';
import { loginAction } from '../redux/modules/registerActions';
import { useDispatch, useSelector } from 'react-redux';
import { setCookie } from '../shared/cookie';

function Login() {
    const dispatch = useDispatch();
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
        event.preventDefault(); // 새로고침 시 폼 제출 동작 방지
        const body = {
            username: id,
            password: pw,
        }

        const response = dispatch(loginAction(body))
            .then((res) => {
                    console.log(res)

                if (res.access) {

                    const cookie = setCookie('refresh', res.refresh, {
                        path: "/",
                        secure: "/",
                    });
                    console.log("cookie", cookie)
                    // navigate("/")
                }
                else {
                    alert("로그인 실패")
                }
            })
            .catch((error) => {
                alert(error)
            })
    }


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
