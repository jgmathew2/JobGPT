import './App.css'
import 'bulma/css/bulma.min.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import MenuPage from './pages/MenuPage';
import FormPage from './pages/FormPage';
import StatusPage from './pages/StatusPage';
import LinkedInForm from './pages/LinkedInForm';
import WorkDayForm from './pages/WorkDayForm';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/form" element={<FormPage />} />
        <Route path="/menu" element={<MenuPage />} />
        <Route path="/linkedin" element={<LinkedInForm />} />
        <Route path="/workday" element={<WorkDayForm />} />
        <Route path="/statuslinkedin" element={<StatusPage isLinkedIn={true} />} />
        <Route path="/statusworkday" element={<StatusPage isLinkedIn={false} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App