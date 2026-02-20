import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Landing from './pages/Landing';

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Landing />
      </main>
      <Footer />
    </div>
  );
}
