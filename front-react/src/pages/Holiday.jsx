import React, { useEffect, useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { getHoliday } from '../apis/apis';
import { Container } from 'react-bootstrap';

const Holiday = () => {
    const [holidayList, setHolidayList] = useState([]);
    const [selectedDate, setSelectedDate] = useState(new Date());

    useEffect(() => {
        const fetchgetHoliday = async () => {
            const res = await getHoliday();
            setHolidayList(res);
        }
        fetchgetHoliday();
    }, []);

    const tileContent = ({ date, view }) => {
        if (view === 'month') {
            const dateString = date.toISOString().split('T')[0];
            const holiday = holidayList.find(holiday => holiday.date === dateString);
            return holiday ? (
                <div style={{ color: 'red' }}>
                    <strong>{holiday.date_name}</strong>
                    {holiday.is_hospital_holiday && <p>병원 휴일</p>}
                    {holiday.is_public_holiday && <p>공휴일</p>}
                </div>
            ) : null;
        }
    };

    return (
        <div>
            <Container>
            <h2>휴일 목록</h2>
            <Calendar
                onChange={setSelectedDate}
                value={selectedDate}
                tileContent={tileContent}
            />
            </Container>
        </div>
    );
};

export default Holiday;
