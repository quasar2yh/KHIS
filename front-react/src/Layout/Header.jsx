import { useState } from 'react';
import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap';

function Header() {
    const [isLoggedIn, setIsLoggedIn] = useState(true);

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
                            <NavDropdown.Item href="#action/3.1">외과</NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.3">내과</NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.3">치과</NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.3">나중에 List로 관리</NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                    <Nav className="ml-auto">
                        {isLoggedIn ? (
                            <Nav.Link href="/login">로그인</Nav.Link>
                        ) : (
                            <NavDropdown title="Profile" id="basic-nav-dropdown">
                                <NavDropdown.Item href="#action/3.1">내 정보</NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.2">예약 현황</NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.3">로그아웃</NavDropdown.Item>
                            </NavDropdown>
                        )}
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}

export default Header;
