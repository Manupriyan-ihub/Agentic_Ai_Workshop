import { ToastContainer } from 'react-toastify';
import { Button } from './components/ui/button';
import AppRouter from './routes';

function App() {
  return (
    <>
      <ToastContainer />
      <AppRouter />
    </>
  );
}

export default App;
