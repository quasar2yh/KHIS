import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap';
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from "js-cookie";
import { useDispatch, useSelector } from 'react-redux';
import { getDepartmentListAction } from '../redux/modules/departmentActions';

function Header() {
    const departmentList = useSelector(state => state.departmentReducer.departmentList);
    const refresh = Cookies.get("refresh");
    const navigate = useNavigate();
    const dispatch = useDispatch();

    useEffect(() => {
        if (departmentList === null) {
            dispatch(getDepartmentListAction());
        }
    }, [departmentList, dispatch])

    const handleLogout = () => {
        Cookies.remove('access', { path: '/' });
        Cookies.remove('refresh', { path: '/' });
        navigate('/login');
    };

    return (
        <Navbar expand="lg" className="bg-body-tertiary">
            <Container>
                <Navbar.Brand href="/">KHIS</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link href="/appointment">Appointment</Nav.Link>
                        <Nav.Link href="/schedule">Schedule</Nav.Link>
                        <NavDropdown title="Department" id="basic-nav-dropdown">
                            {departmentList && departmentList.map((department => {
                                return <NavDropdown.Item href="/" key={department.id}>{department.department}</NavDropdown.Item>
                            }))}
                        </NavDropdown>
                        <Nav.Link href="/chatbot">Chatbot</Nav.Link>
                    </Nav>
                    <Nav className="ml-auto">
                        {refresh ? (
                            <NavDropdown title="Profile" id="profile-nav-dropdown">
                                <NavDropdown.Item href="/profile">내 정보</NavDropdown.Item>
                                <NavDropdown.Item href="/appointmentstatus">예약 현황</NavDropdown.Item>
                                <NavDropdown.Item onClick={handleLogout}>로그아웃</NavDropdown.Item>
                            </NavDropdown>
                        ) : (
                            <Nav.Link href="/login">로그인</Nav.Link>
                        )}
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}

export default Header;
