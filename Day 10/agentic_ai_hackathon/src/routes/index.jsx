import Login from '@/pages/auth/Login';
import HomePage from '@/pages/Home';
import TaskSubmission from '@/pages/TaskSubmission';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<HomePage />} />
        <Route path="/task-submission" element={<TaskSubmission />} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRouter;
