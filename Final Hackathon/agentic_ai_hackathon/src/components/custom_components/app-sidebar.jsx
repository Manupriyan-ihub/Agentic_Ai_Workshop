import {
  CheckCheckIcon,
  LayoutDashboard,
  Upload,
  FileText,
  Users,
  Settings,
} from 'lucide-react';
import { NavMain } from './nav-main';
import { NavUser } from './nav-user';
import { NavLink } from 'react-router-dom';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarRail,
} from '@/components/ui/sidebar';
import { useSelector } from 'react-redux';

export function AppSidebar({ setPageName, isCollapsed, ...props }) {
  const user = useSelector((state) => state.auth.user);

  // Define sidebar navigation items
  const navigationItems = [
    // {
    //   path: '/user/dashboard',
    //   label: 'Dashboard',
    //   icon: LayoutDashboard,
    // },
    {
      path: '/user/task-submission',
      label: 'Task Submission',
      icon: Upload,
    },
  ];

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <div className="flex items-center gap-3">
          <CheckCheckIcon className="h-8 w-8" />
          {isCollapsed && (
            <span className="text-3xl font-extrabold">Hackathon</span>
          )}
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarMenu className="gap-1 px-5 py-6 group-data-[collapsible=icon]:px-4">
          {navigationItems.map((item) => (
            <SidebarMenuItem key={item.path}>
              <NavLink to={item.path}>
                {({ isActive }) => (
                  <SidebarMenuButton
                    tooltip={item.label}
                    isActive={isActive}
                    className={`text-color1 flex min-h-[2.5rem] w-full items-center justify-start gap-3 rounded-lg transition-all duration-200 ease-in-out group-data-[collapsible=icon]:flex-col group-data-[collapsible=icon]:items-center group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:gap-1 ${
                      isActive
                        ? 'from-primary bg-gradient-to-r to-blue-600 text-white [&>svg]:text-white'
                        : 'hover:text-primary hover:bg-blue-100'
                    }`}
                    onClick={() => setPageName(item.label)}
                  >
                    <item.icon className="h-6 w-6 group-data-[collapsible=icon]:h-5 group-data-[collapsible=icon]:w-5" />
                    <span
                      className={`text-sm font-medium group-data-[collapsible=icon]:hidden ${
                        isActive ? 'text-white' : ''
                      }`}
                    >
                      {item.label}
                    </span>
                  </SidebarMenuButton>
                )}
              </NavLink>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarContent>

      <SidebarFooter>
        <NavUser user={user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
