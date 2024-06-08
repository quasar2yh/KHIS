import { Container, Navbar } from 'react-bootstrap';
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from "js-cookie";
import { useDispatch, useSelector } from 'react-redux';
import { getDepartmentListAction } from '../redux/modules/departmentActions';
import PatientMenu from '../components/patient/PatientMenu';
import PractitionerMenu from '../components/practitioner/PractitionerMenu';
import { resetUserAction } from '../redux/modules/userActions';

function Header() {
    const accountInfo = useSelector(state => state.userReducer.accountInfo);
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
        dispatch(resetUserAction());
        navigate('/login');
    };

    console.log("accountInfo", accountInfo)

    return (<>
        <Navbar expand="lg" className="bg-body-tertiary">
            <Container>
                {accountInfo && accountInfo.subject === 'Practitioner'
                    ? <PractitionerMenu refresh={refresh} handleLogout={handleLogout} />
                    : <PatientMenu refresh={refresh} handleLogout={handleLogout} />}
            </Container>
        </Navbar >
    </>);
}

export default Header;