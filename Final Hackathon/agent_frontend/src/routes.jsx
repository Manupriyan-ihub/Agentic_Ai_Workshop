import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import TaskSubmission from "./pages/TaskSubmission";
export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="/task-submission" element={<TaskSubmission />} />
      </Route>
    </Routes>
  );
}
