import React from 'react';

interface HeaderProps {
  username: string;
}

const Header: React.FC<HeaderProps> = ({ username }) => {
  return (
    <header className="bg-primary text-white p-4">
      <div className="container mx-auto">
        <h1 className="text-2xl font-bold">Welcome, {username}!</h1>
      </div>
    </header>
  );
};

export default Header;
