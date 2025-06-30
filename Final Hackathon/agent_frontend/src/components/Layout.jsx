import { Outlet, Link, useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import { LayoutDashboardIcon, ListTodoIcon, LogOutIcon } from "lucide-react";

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const navigation = [
    { name: "Dashboard", href: "/dashboard", icon: <LayoutDashboardIcon /> },
    {
      name: "Task Submission",
      href: "/task-submission",
      icon: <ListTodoIcon />,
    },
  ];

  const isActive = (href) => {
    if (href === "/") {
      return location.pathname === "/";
    }
    return location.pathname.startsWith(href);
  };

  const handleLogout = () => {
    localStorage.removeItem("userData");
    // setIsLoggedIn(false);
    navigate("/"); // Adjust the route as needed
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-cyan-50 flex">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden backdrop-blur-sm"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-gradient-to-b from-slate-900 via-purple-900 to-indigo-900
        transform transition-all duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0
        shadow-2xl backdrop-blur-xl border-r border-purple-500/20
        ${sidebarOpen ? "translate-x-0" : "-translate-x-full"}
      `}
      >
        <div className="flex flex-col h-full relative">
          {/* Gradient overlay for glass effect */}
          <div className="absolute inset-0 bg-gradient-to-b from-purple-600/10 to-transparent pointer-events-none"></div>

          {/* Logo/Brand */}
          <div className="flex items-center justify-between p-6 border-b border-purple-500/30 relative z-10">
            <Link
              to="/"
              className="text-2xl font-bold bg-gradient-to-r from-purple-300 to-cyan-300 bg-clip-text text-transparent hover:from-purple-200 hover:to-cyan-200 transition-all duration-300"
            >
              Linkedin Verifier
            </Link>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden text-purple-200 hover:text-white transition-colors duration-200 hover:bg-purple-700/30 rounded-lg p-1"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2 relative z-10">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                onClick={() => setSidebarOpen(false)}
                className={`
                  group flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-300
                  ${
                    isActive(item.href)
                      ? "bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-500/25 transform scale-105 border border-purple-400/30"
                      : "text-purple-100 hover:bg-gradient-to-r hover:from-purple-700/50 hover:to-indigo-700/50 hover:text-white hover:shadow-lg hover:shadow-purple-500/20 hover:transform hover:scale-105 hover:border hover:border-purple-400/20"
                  }
                `}
              >
                <span className="text-xl mr-3 group-hover:scale-110 transition-transform duration-200">
                  {item.icon}
                </span>
                {item.name}
                {isActive(item.href) && (
                  <div className="ml-auto w-2 h-2 bg-cyan-300 rounded-full animate-pulse"></div>
                )}
              </Link>
            ))}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-purple-500/30 relative z-10">
            <div className="text-xs text-purple-200 text-center bg-purple-800/20 rounded-lg py-2 px-3 backdrop-blur-sm">
              {/* © 2025 GenAI Hackathon */}
              <button
                onClick={handleLogout}
                className="px-6 py-3 w-full flex items-center rounded-2xl gap-5  bg-gradient-to-r from-purple-600 to-indigo-600 text-white text-xl shadow-lg shadow-purple-500/25 transform scale-105 border border-purple-400/30"
              >
                <LogOutIcon />
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col lg:ml-0">
        {/* Top bar for mobile */}
        <header className="lg:hidden bg-white/80 backdrop-blur-xl shadow-lg border-b border-purple-200/30 p-4 flex items-center justify-between">
          <button
            onClick={() => setSidebarOpen(true)}
            className="text-slate-600 hover:text-purple-600 transition-colors duration-200 hover:bg-purple-100 rounded-lg p-2"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
          <h1 className="text-lg font-semibold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
            GenAI Hackathon
          </h1>
          <div className="w-10"></div>
        </header>

        {/* Page content */}
        <main className="flex-1 p-6">
          <div className="bg-white/60 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6 min-h-full">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
