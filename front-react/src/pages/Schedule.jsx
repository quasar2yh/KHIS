import React, { useEffect, useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { getHoliday } from '../apis/apis';
import { Container } from 'react-bootstrap';

function Schedule() {
    const [holidayList, setHolidayList] = useState([]);
    const [selectedDate, setSelectedDate] = useState(new Date());

    useEffect(() => {
        const fetchgetHoliday = async () => {
            const res = await getHoliday();
            setHolidayList(res);
        }
        fetchgetHoliday();
    }, []);

    console.log("holidayList", holidayList)

    const tileContent = ({ date, view }) => {
        if (view === 'month') {

            // console.log("date", date)
            const dateString = date.toISOString().split('T')[0];
            // console.log("dateString", dateString)

            const holiday = holidayList.find((holiday) => {
                return holiday.date === dateString
            });
            return holiday ? (
                <div style={{ color: 'red' }}>
                    <strong>{holiday.date_name}</strong>
                    {holiday.is_hospital_holiday && <p>병원 휴일</p>}
                    {holiday.is_public_holiday && <p>공휴일</p>}
                </div>
            ) : null;
        }
    };

    console.log("selectedDate", selectedDate)
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

export default Schedule;
