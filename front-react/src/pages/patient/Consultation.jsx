import React, { useState, useEffect } from 'react';
import { getConsultations } from '../../apis/apis';
import { useSelector } from 'react-redux';
import ConsultationList from '../../components/ConsultationList';

function Consultation() {
    const accountInfo = useSelector(state => state.userReducer.accountInfo);
    const [consultations, setConsultations] = useState(null);
    const [selectConsultation, setSelectedConsultation] = useState(null);
    const [show, setShow] = useState(false);

    useEffect(() => {
        if (accountInfo && accountInfo.subject === 'Patient') {
            getConsultations(accountInfo.patient).then(res=> {
                setConsultations(res)
            });
        }
    }, [accountInfo]);


    const handleClose = () => setShow(false);
    const handleShow = (consoltation) => {
        setSelectedConsultation(consoltation);
        setShow(true);
    };

    return (<>
        <ConsultationList 
        consultations={consultations}
        selectConsultation={selectConsultation}
        show={show}
        handleClose={handleClose}
        handleShow={handleShow}
        />
        </>);
}

export default Consultation;
