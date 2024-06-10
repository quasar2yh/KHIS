import React from 'react';
import { Link } from "react-router-dom";
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';
import { useSelector } from 'react-redux';

function PatientMenu({ handleLogout }) {
    const accountInfo = useSelector(state => state.userReducer.accountInfo);
    const departmentList = useSelector(state => state.departmentReducer.departmentList) || [];

    return (
        <>
            <Navbar.Brand href="/">KHIS</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                    <Nav.Link href="/appointment">예약하기</Nav.Link>
                    
                    <Nav.Link href="/schedule">병원 휴일</Nav.Link>
                    <NavDropdown title="진료과" id="basic-nav-dropdown">
                        {Array.isArray(departmentList) && departmentList.map(department => (
                            <NavDropdown.Item href={`/department/${department.id}`} key={department.id}>
                                {department.department_name}
                            </NavDropdown.Item>
                        ))}
                    </NavDropdown>
                    <Nav.Link href="/chatbot">Chatbot</Nav.Link>
                </Nav>
                <Nav className="ml-auto">
                    {accountInfo ? (
                        <NavDropdown title="Profile" id="profile-nav-dropdown">
                            <NavDropdown.Item as={Link} to="/profile">내 정보</NavDropdown.Item>
                            <NavDropdown.Item href="/appointmentstatus">예약 현황</NavDropdown.Item>
                            {accountInfo && accountInfo.subject === 'Patient' && (
                                <NavDropdown.Item href="/consultation">진료 기록</NavDropdown.Item>
                            )}
                            <NavDropdown.Item onClick={handleLogout}>로그아웃</NavDropdown.Item>
                        </NavDropdown>
                    ) : (
                        <Nav.Link href="/login">로그인</Nav.Link>
                    )}
                </Nav>
            </Navbar.Collapse>
        </>
    )
};

export default PatientMenu;
