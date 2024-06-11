import React, { useEffect, useState } from 'react';
import { getWaitingList } from '../apis/apis';

const WaitingList = () => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const data = await getWaitingList();
        setAppointments(data.results);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching waiting list:', error);
        setLoading(false);
      }
    };

    fetchAppointments();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Waiting List</h1>
      <ul>
        {appointments.map(appointment => (
          <li key={appointment.id}>
            {appointment.patient_name} - {appointment.start_time}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default WaitingList;
