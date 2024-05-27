import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap';
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';

function Header() {
    const [cookies, setCookie, removeCookie] = useCookies(['access', 'refresh']);
    const refresh = cookies.refresh; // 쿠키 값을 직접 접근
    const navigate = useNavigate();

    const handleLogout = () => {
        removeCookie('access', { path: '/' });
        removeCookie('refresh', { path: '/' });
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
                            <NavDropdown.Item href="#action/3.1">외과</NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.2">내과</NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.3">치과</NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.4">나중에 List로 관리</NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                    <Nav className="ml-auto">
                        {refresh ? (
                            <NavDropdown title="Profile" id="profile-nav-dropdown">
                                <NavDropdown.Item href="#action/3.1">내 정보</NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.2">예약 현황</NavDropdown.Item>
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
