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
import Procedure from "./practitioner/Procedure";
import GetConsultations from "./practitioner/GetConsultations";
import Claim from "./practitioner/Claim";


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
                        <Route path="/medical-record-list" element={<GetConsultations />} />
                        <Route path="/procedure" element={<Procedure />} />
                        <Route path="/annual" element={<Annual />} />
                        <Route path="/claim" element={<Claim />} />
                    </Routes>
                </Layout>
            </TokenRefresher>
        </BrowserRouter>
    );
};

export default Router;
