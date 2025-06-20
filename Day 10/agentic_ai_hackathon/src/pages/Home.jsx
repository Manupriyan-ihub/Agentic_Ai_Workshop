import { Outlet } from 'react-router-dom';
import { Separator } from '@/components/ui/separator';

import {
  SidebarProvider,
  SidebarInset,
  SidebarTrigger,
} from '@/components/ui/sidebar';
import { AppSidebar } from '@/components/custom_components/app-sidebar';
import { useState } from 'react';

const Layout = () => {
  const [isCollapsed, setIsCollapsed] = useState(true);

  const toggle = () => setIsCollapsed((prev) => !prev);
  return (
    <SidebarProvider>
      <AppSidebar isCollapsed={isCollapsed} />

      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
          <div className="flex items-center gap-2 px-4">
            <SidebarTrigger className="-ml-1" onClick={toggle} />
            <Separator
              orientation="vertical"
              className="mr-2 data-[orientation=vertical]:h-4"
            />
          </div>
        </header>

        {/* Main Content */}
        <main className="flex flex-1 flex-col gap-4 p-4 pt-0">
          <Outlet />
          dasdas
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
};

export default Layout;
