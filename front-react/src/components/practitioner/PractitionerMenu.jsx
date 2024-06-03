import React from 'react';
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';

function PractitionerMenu({ refresh, handleLogout }) {

    return (
        <>
            <Navbar.Brand href="/">KHIS</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                    <NavDropdown title="진단">
                        <NavDropdown.Item href="/medical-record">작성</NavDropdown.Item>
                    </NavDropdown>
                    <Nav.Link href="/procedure">수술</Nav.Link>
                    <Nav.Link href="/">일정</Nav.Link>
                    <Nav.Link href="/annual">연차</Nav.Link>
                </Nav>
                <Nav className="ml-auto">
                    {refresh ? (
                        <NavDropdown title="Profile" id="profile-nav-dropdown">
                            <NavDropdown.Item href="/profile">내 정보</NavDropdown.Item>
                            <NavDropdown.Item onClick={handleLogout}>로그아웃</NavDropdown.Item>
                        </NavDropdown>
                    ) : (
                        <Nav.Link href="/login">로그인</Nav.Link>
                    )}
                </Nav>
            </Navbar.Collapse>
        </>
    );
}

export default PractitionerMenu;