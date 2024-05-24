import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "../pages/Home";
import Appointment from "../pages/Appointment";
import Schedule from "../pages/Schedule";
import Layout from "../Layout/Layout";
import Login from "../pages/Login";
import SigninPatient from "../pages/SigninPatient";
import { AuthProvider } from "./contexts";

const Router = () => {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Layout>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/appointment" element={<Appointment />} />
                        <Route path="/schedule" element={<Schedule />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/signin/patient" element={<SigninPatient />} />
                    </Routes>
                </Layout>
            </BrowserRouter>
        </AuthProvider>
    );
};

export default Router;
