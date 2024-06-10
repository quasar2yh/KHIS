import { Container, Navbar } from 'react-bootstrap';
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { getDepartmentListAction } from '../redux/modules/departmentActions';
import PatientMenu from '../components/patient/PatientMenu';
import PractitionerMenu from '../components/practitioner/PractitionerMenu';
import { logoutAction } from '../apis/apis';
import { resetUserAction } from '../redux/modules/userActions';

function Header() {
    const accountInfo = useSelector(state => state.userReducer.accountInfo);
    const departmentList = useSelector(state => state.departmentReducer.departmentList);
    const navigate = useNavigate();
    const dispatch = useDispatch();

    useEffect(() => {
        if (departmentList === null) {
            dispatch(getDepartmentListAction());
        }
    }, [departmentList, dispatch])


    const handleLogout = () => {
        logoutAction();
        dispatch(resetUserAction());
        navigate('/login');
    };

    return (<>
        <Navbar expand="lg" className="bg-body-tertiary">
            <Container>
                {accountInfo && accountInfo.subject === 'Practitioner'
                    ? <PractitionerMenu handleLogout={handleLogout} />
                    : <PatientMenu handleLogout={handleLogout} />}
            </Container>
        </Navbar >
    </>);
}

export default Header;