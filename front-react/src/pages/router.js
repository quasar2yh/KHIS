import { BrowserRouter, Route, Routes } from "react-router-dom";
import TokenRefresher from "../components/TokenRefresher";
import Home from "./Home";
import Appointment from "./patient/Appointment";
import Layout from "../Layout/Layout";
import Login from "./Login";
import SelectRegisterForm from "./Register";
import Profile from "./Profile";
import AppoinmentStatus from "./patient/AppoinmentStatus";
import Chatbot from "./Chatbot";
import Department from "./Department";
import Consultation from "./patient/Consultation";
import PostConsultation from "./practitioner/PostConsultation";
import Annual from "./practitioner/Annual";
import Schedule from "./Schedule";


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
                        <Route path="/chatbot" element={<Chatbot />} />
                        <Route path="/department/:id" element={<Department />} />
                        <Route path="/consultation" element={<Consultation />} />
                        <Route path="/medical-record" element={<PostConsultation />} />
                        <Route path="/annual" element={<Annual />} />
                    </Routes>
                </Layout>
            </TokenRefresher>
        </BrowserRouter>
    );
};

export default Router;
