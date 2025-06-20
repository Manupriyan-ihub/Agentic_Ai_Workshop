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

export function AppSidebar({ isCollapsed, ...props }) {
  const user = useSelector((state) => state.auth.user);

  // Define sidebar navigation items
  const navigationItems = [
    {
      path: '/dashboard',
      label: 'Dashboard',
      icon: LayoutDashboard,
    },
    {
      path: '/task-submission',
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
                    className={`text-color1 hover:text-primary min-h-[2.5rem] w-full group-data-[collapsible=icon]:justify-center hover:bg-blue-50 ${
                      isActive
                        ? 'bg-gradient-custom text-white hover:text-white [&>svg]:text-white'
                        : 'hover:text-primary hover:bg-blue-50'
                    }`}
                  >
                    <item.icon className="h-6 w-6 group-data-[collapsible=icon]:h-5 group-data-[collapsible=icon]:w-5" />
                    <span className="text-sm font-medium group-data-[collapsible=icon]:hidden">
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
