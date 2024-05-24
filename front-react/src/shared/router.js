import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "../pages/Home";
import Appointment from "../pages/Appointment";
import Schedule from "../pages/Schedule";
import Layout from "../Layout/Layout";
import Login from "../pages/Login";
import SigninPatient from "../pages/SigninPatient";

const Router = () => {
    return (
        < BrowserRouter >
            <Layout>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/appointment" element={<Appointment />} />
                    <Route path="/schedule" element={<Schedule />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/signin/patient" element={<SigninPatient />} />
                </Routes>
            </Layout>
        </BrowserRouter >
    );
};

export default Router