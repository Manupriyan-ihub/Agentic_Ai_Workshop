import { LoginForm } from '@/components/custom_components/login-form';
import { CheckCheckIcon } from 'lucide-react';

export default function LoginPage() {
  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      <div className="flex flex-col items-center justify-center p-6 md:p-10">
        <div className="w-full max-w-sm">
          <div className="mb-8 flex flex-col items-center gap-2">
            <CheckCheckIcon className="size-8" />
            <h1 className="text-3xl font-bold">OKRion</h1>
            <p className="text-muted-foreground">Welcome back</p>
          </div>
          <LoginForm />
        </div>
      </div>
      <div className="bg-muted relative hidden lg:block">
        <img
          src="https://images.unsplash.com/photo-1590069261209-f8e9b8642343?q=80&w=1976&auto=format&fit=crop"
          alt="A beautiful workspace"
          className="absolute inset-0 h-full w-full object-cover dark:brightness-[0.3]"
          onError={(e) => {
            e.target.onerror = null;
            e.target.src =
              'https://placehold.co/1080x1920/18181b/ffffff?text=Image';
          }}
        />
      </div>
    </div>
  );
}
