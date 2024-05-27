import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "../pages/Home";
import Appointment from "../pages/Appointment";
import Schedule from "../pages/Schedule";
import Layout from "../Layout/Layout";
import Login from "../pages/Login";
import PatientRegister from "../pages/PatientRegister";
import TokenRefresher from "../components/TokenRefresher";
import { CookiesProvider } from 'react-cookie';

const Router = () => {
    return (
        <BrowserRouter>
            <CookiesProvider>
                <TokenRefresher>
                    <Layout>
                        <Routes>
                            <Route path="/" element={<Home />} />
                            <Route path="/appointment" element={<Appointment />} />
                            <Route path="/schedule" element={<Schedule />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/register/patient" element={<PatientRegister />} />
                        </Routes>
                    </Layout>
                </TokenRefresher>
            </CookiesProvider>
        </BrowserRouter>
    );
};

export default Router;
