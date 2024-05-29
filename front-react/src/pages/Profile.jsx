import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card, ListGroup, Button } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { getPatientInfoAction, getPractitionerInfoAction } from '../redux/modules/userActions';
import Account from '../components/Account';
import ProfileUpdate from '../components/ProfileUpdate';
import PractitionerProfileUpdate from '../components/PractitionerProfileUpdate';

function Profile() {
    const AccountInfo = useSelector(state => state.userReducer.AccountInfo);
    const patientInfo = useSelector(state => state.userReducer.patientInfo);
    const practitionerInfo = useSelector(state => state.userReducer.practitionerInfo);
    const dispatch = useDispatch();

    const [showPatientProfileUpdate, setShowPatientProfileUpdate] = useState(false);
    const [showPractitionerProfileUpdate, setShowPractitionerProfileUpdate] = useState(false);

    useEffect(() => {
        if (AccountInfo && AccountInfo.subject === 'Patient' && !patientInfo) {
            dispatch(getPatientInfoAction(AccountInfo.patient));
        } else if (AccountInfo && AccountInfo.subject === 'Practitioner' && !practitionerInfo) {
            dispatch(getPractitionerInfoAction(AccountInfo.practitioner));
        }
    }, [dispatch, AccountInfo, patientInfo, practitionerInfo]);

    if (!patientInfo && !practitionerInfo) {
        return <div>Loading...</div>;
    }

    const onClose = () => {
        setShowPatientProfileUpdate(false);
        setShowPractitionerProfileUpdate(false);
    };

    const renderProfile = (info, isPatient) => {
        const fields = isPatient
            ? [
                { label: 'Name', value: info.name ? `${info.name.family} ${info.name.name}` : 'N/A' },
                { label: 'Gender', value: info.gender || 'N/A' },
                { label: 'Allergies', value: info.allergies || 'None' },
                { label: 'Telecom', value: info.telecom ? info.telecom.value : 'N/A' },
                { label: 'Address', value: info.address ? `${info.address.city} ${info.address.text}` : 'N/A' }
            ]
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
