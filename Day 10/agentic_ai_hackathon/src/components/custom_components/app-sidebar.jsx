import { CheckCheckIcon, Frame, Map, PieChart } from 'lucide-react';
import { NavMain } from './nav-main';
import { NavUser } from './nav-user';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarRail,
} from '@/components/ui/sidebar';
import { useSelector } from 'react-redux';

export function AppSidebar({ isCollapsed, ...props }) {
  const user = useSelector((state) => state.auth.user);

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <div className="flex items-center gap-3">
          <CheckCheckIcon />{' '}
          {isCollapsed && (
            <span className="text-3xl font-extrabold">Hackathon</span>
          )}
        </div>
      </SidebarHeader>
      <SidebarContent>
        {/* <SidebarMenu className="gap-1 px-5 py-6 group-data-[collapsible=icon]:px-4">
          {items.map((item, index) => (
            <React.Fragment key={item.path}>
              <SidebarMenuItem>
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

              {role === 'coordinator' && index === 4 && (
                <SidebarSeparator className="bg-color8 my-2" />
              )}
            </React.Fragment>
          ))}
        </SidebarMenu> */}
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
