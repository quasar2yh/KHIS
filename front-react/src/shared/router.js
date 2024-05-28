import { BrowserRouter, Route, Routes } from "react-router-dom";
import TokenRefresher from "../components/TokenRefresher";
import Home from "../pages/Home";
import Appointment from "../pages/Appointment";
import Schedule from "../pages/Schedule";
import Layout from "../Layout/Layout";
import Login from "../pages/Login";
import SelectRegisterForm from "../pages/Register";


const Router = () => {
    return (
        <BrowserRouter>
                <TokenRefresher>
                    <Layout>
                        <Routes>
                            <Route path="/" element={<Home />} />
                            <Route path="/appointment" element={<Appointment />} />
                            <Route path="/schedule" element={<Schedule />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/register" element={<SelectRegisterForm />} />
                        </Routes>
                    </Layout>
                </TokenRefresher>
        </BrowserRouter>
    );
};

export default Router;
