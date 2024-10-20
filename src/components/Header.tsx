import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Sun, Moon, User } from 'lucide-react';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import { useSession, signOut } from 'next-auth/react';

const Header: React.FC = () => {
  const [darkMode, setDarkMode] = useState(false);
  const { data: session } = useSession();

  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="font-heading text-2xl font-bold text-primary">
          FakeProfileDetector
        </Link>
        <nav>
          <ul className="flex space-x-6">
            {session ? (
              <>
                <li><Link to="/dashboard" className="hover:text-primary transition duration-300">Dashboard</Link></li>
                <li><Link to="/analysis" className="hover:text-primary transition duration-300">Analyze</Link></li>
                <li><Link to="/history" className="hover:text-primary transition duration-300">History</Link></li>
              </>
            ) : (
              <>
                <li><Link to="/login" className="hover:text-primary transition duration-300">Login</Link></li>
                <li><Link to="/register" className="hover:text-primary transition duration-300">Register</Link></li>
              </>
            )}
          </ul>
        </nav>
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="p-2 rounded-full hover:bg-gray-200 transition duration-300"
          >
            {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
          {session && (
            <DropdownMenu.Root>
              <DropdownMenu.Trigger asChild>
                <button className="p-2 rounded-full hover:bg-gray-200 transition duration-300">
                  <User className="w-5 h-5" />
                </button>
              </DropdownMenu.Trigger>
              <DropdownMenu.Content className="bg-white shadow-lg rounded-md p-2 mt-2">
                <DropdownMenu.Item className="p-2 hover:bg-gray-100 cursor-pointer">Profile</DropdownMenu.Item>
                <DropdownMenu.Item className="p-2 hover:bg-gray-100 cursor-pointer">Settings</DropdownMenu.Item>
                <DropdownMenu.Item className="p-2 hover:bg-gray-100 cursor-pointer" onSelect={() => signOut()}>
                  Logout
                </DropdownMenu.Item>
              </DropdownMenu.Content>
            </DropdownMenu.Root>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;