import React, { useEffect, useState } from 'react';
import { getWaitingList, getPatientInfo, getDepartments } from '../apis/apis'; // getPatientInfo, getDepartments 함수는 각각 환자 정보와 부서 정보를 가져오는 API 호출을 처리하는 함수입니다.

const WaitingList = () => {
  const [appointments, setAppointments] = useState([]);
  const [departments, setDepartments] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const waitingListData = await getWaitingList();
        const departmentData = await getDepartments();

        const departmentsObj = {};
        departmentData.forEach(department => {
          departmentsObj[department.id] = department.department_name;
        });

        setDepartments(departmentsObj);

        const appointmentsWithInfo = await Promise.all(waitingListData.results.map(async appointment => {
          const patientInfo = await getPatientInfo(appointment.patient);
          return { ...appointment, patient: patientInfo };
        }));

        setAppointments(appointmentsWithInfo);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4">Waiting List</h1>
      <ul className="list-group">
        {appointments.map(appointment => (
          <li key={appointment.id} className="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <span className="fw-bold">{appointment.patient?.name?.family}{appointment.patient?.name?.name}</span> - {new Date(appointment.start).toLocaleString()}
            </div>
            <div>
              {departments[appointment.department]}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default WaitingList;
