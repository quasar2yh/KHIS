import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card, ListGroup, Button } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { getPatientInfoAction, getPractitionerInfoAction } from '../redux/modules/userActions';
import Account from '../components/Account';
import ProfileUpdate from '../components/patient/ProfileUpdate';
import PractitionerProfileUpdate from '../components/practitioner/PractitionerProfileUpdate';

function Profile() {
    const AccountInfo = useSelector(state => state.userReducer.AccountInfo);
    const patientInfo = useSelector(state => state.userReducer.patientInfo);
    const practitionerInfo = useSelector(state => state.userReducer.practitionerInfo);
    const dispatch = useDispatch();

    // 프로필 수정 컴포넌트를 보여주기 위한 변수
    // true면 해당 컴포넌트 렌더링
    const [showPatientProfileUpdate, setShowPatientProfileUpdate] = useState(false);
    const [showPractitionerProfileUpdate, setShowPractitionerProfileUpdate] = useState(false);

    useEffect(() => {
        // AccounInfo가 환자면 환자 정보 가져오는 Reducer Action 실행
        if (AccountInfo && AccountInfo.subject === 'Patient' && !patientInfo) {
            dispatch(getPatientInfoAction(AccountInfo.patient));
        
        // AccounInfo가 의료진이면 의료진 정보 가져오는 Reducer Action 실행
        } else if (AccountInfo && AccountInfo.subject === 'Practitioner' && !practitionerInfo) {
            dispatch(getPractitionerInfoAction(AccountInfo.practitioner));
        }
    }, [dispatch, AccountInfo, patientInfo, practitionerInfo]);


    // Info가 없으면 Loading... 렌더링
    if (!patientInfo && !practitionerInfo) {
        return <div>Loading...</div>;
    }

    // 프로필 수정하는 컴포넌트를 닫기 위한 함수
    const onClose = () => {
        setShowPatientProfileUpdate(false);
        setShowPractitionerProfileUpdate(false);
    };

    // info와 isPatient를 인자로 받아 프로필 랜더링
    const renderProfile = (info, isPatient) => {
        const fields = isPatient
        // isPatient === True
            ? [
                { label: 'Name', value: info.name ? `${info.name.family} ${info.name.name}` : 'N/A' },
                { label: 'Gender', value: info.gender || 'N/A' },
                { label: 'Allergies', value: info.allergies || 'None' },
                { label: 'Telecom', value: info.telecom ? info.telecom.value : 'N/A' },
                { label: 'Address', value: info.address ? `${info.address.city} ${info.address.text}` : 'N/A' }
            ]
        // isPatient === False
            : [
                { label: 'Name', value: info.name ? `${info.name.family} ${info.name.name}` : 'N/A' },
                { label: 'Gender', value: info.gender || 'N/A' },
                { label: 'Birth Date', value: info.birth_date || 'N/A' },
                { label: 'License Type', value: info.license_type || 'N/A' },
                { label: 'License Number', value: info.license_number || 'N/A' },
                { label: 'Role', value: info.role || 'N/A' },
                { label: 'Rank', value: info.rank || 'N/A' },
                { label: 'Telecom', value: info.telecom ? info.telecom.value : 'N/A' },
                { label: 'Address', value: info.address ? `${info.address.city} ${info.address.text}` : 'N/A' },
                { label: 'Department', value: info.department || 'N/A' }
            ];

        return (
            <Container className="mt-5">
                <Row className="justify-content-center">
                    <Col md={8}>
                        <Card>
                            <Card.Header as="h4" className="bg-primary text-white text-center">
                                Profile
                            </Card.Header>
                            <Card.Body>
                                <ListGroup variant="flush">
                                    {fields.map((field, index) => (
                                        <ListGroup.Item key={index}>
                                            <Row>
                                                <Col md={4} className="text-right font-weight-bold">{field.label}:</Col>
                                                <Col md={8}>{field.value}</Col>
                                            </Row>
                                        </ListGroup.Item>
                                    ))}
                                </ListGroup>
                                <Button variant="primary" className="mt-3" onClick={() => {
                                    // isPatient가 True면 환자 프로필 수정 컴포넌트 랜더링
                                    // ispatient가 False면 의료진 프로필 수정 컴포넌트 랜더링
                                    isPatient ? setShowPatientProfileUpdate(true) : setShowPractitionerProfileUpdate(true);
                                }}>
                                    Update
                                </Button>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        );
    };

    return (
        <> 
            {showPatientProfileUpdate && <ProfileUpdate onClose={onClose} />}
            {showPractitionerProfileUpdate && <PractitionerProfileUpdate onClose={onClose} />}
            {!showPatientProfileUpdate && !showPractitionerProfileUpdate && (
                <>
                    {patientInfo ? renderProfile(patientInfo, true) : renderProfile(practitionerInfo, false)}
                </>
            )}
            <Account />
        </>
    );
}

export default Profile;
