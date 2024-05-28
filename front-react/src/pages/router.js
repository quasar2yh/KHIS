import { BrowserRouter, Route, Routes } from "react-router-dom";
import TokenRefresher from "../components/TokenRefresher";
import Home from "./Home";
import Appointment from "./Appointment";
import Schedule from "./Schedule";
import Layout from "../Layout/Layout";
import Login from "./Login";
import SelectRegisterForm from "./Register";
import Profile from "./Profile";
import AppoinmentStatus from "./AppoinmentStatus";


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
                            <Route path="/profile" element={<Profile />} />
                            <Route path="/appointmentstatus" element={<AppoinmentStatus />} />
                        </Routes>
                    </Layout>
                </TokenRefresher>
        </BrowserRouter>
    );
};

export default Router;
