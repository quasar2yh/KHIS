import React from 'react';
import { useDaumPostcodePopup } from 'react-daum-postcode';
import { Button } from 'react-bootstrap';

const Postcode = ({ formData, setFormData }) => {
  const open = useDaumPostcodePopup();

  const handleComplete = (data) => {
    setFormData({
      ...formData,
      address: {
        ...formData.address,
        city: data.roadAddress,
        postal_code: data.zonecode
      }
    });
  };

  const handleClick = () => {
    open({ onComplete: handleComplete });
  };

  return (
    <Button variant="outline-primary" size="sm" onClick={handleClick}>
      주소 검색
    </Button>
  );
};

export default Postcode;
