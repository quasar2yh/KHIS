import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Link } from 'react-router-dom';
import IdPwForm from '../components/IdPwForm';
import { useDispatch } from 'react-redux';

function Login() {
    const dispatch = useDispatch();

    const [id, setId] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [msg, setMsg] = useState("");

    useEffect(() => {

    }, [msg])

    const LoginFunc = (event) => {
        event.preventDefault();
    }

    return (
        <Form className="d-flex flex-column align-items-center" onSubmit={LoginFunc}>
            <IdPwForm onChange={handleChange} />
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
