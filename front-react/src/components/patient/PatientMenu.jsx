import React from 'react';
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';
import { useSelector } from 'react-redux';

function PatientMenu({ refresh, handleLogout }) {
    const AccountInfo = useSelector(state => state.userReducer.AccountInfo);
    const departmentList = useSelector(state => state.departmentReducer.departmentList);

    return (
        <>
            <Navbar.Brand href="/">KHIS</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                    <Nav.Link href="/appointment">Appointment</Nav.Link>
                    <Nav.Link href="/schedule">Schedule</Nav.Link>
                    <Nav.Link href="/holiday">Holiday</Nav.Link>
                    <NavDropdown title="Department" id="basic-nav-dropdown">
                        {departmentList && departmentList.map((department => {
                            return <NavDropdown.Item href={`/department/${department.id}`} key={department.id}>{department.department_name}</NavDropdown.Item>
                        }))}
                    </NavDropdown>
                    <Nav.Link href="/chatbot">Chatbot</Nav.Link>
                </Nav>
                <Nav className="ml-auto">
                    {refresh ? (
                        <NavDropdown title="Profile" id="profile-nav-dropdown">
                            <NavDropdown.Item href="/profile">내 정보</NavDropdown.Item>
                            <NavDropdown.Item href="/appointmentstatus">예약 현황</NavDropdown.Item>
                            {AccountInfo && AccountInfo.subject === 'Patient' && (
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