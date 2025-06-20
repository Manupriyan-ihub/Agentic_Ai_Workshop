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
  return <h1>Title</h1>;
};

export default Layout;
