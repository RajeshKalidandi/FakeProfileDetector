import React, { useState, useEffect } from 'react';
import { User } from '../lib/types';

const AdminDashboard: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [stats, setStats] = useState({
    totalUsers: 0,
    proUsers: 0,
    totalScans: 0,
    totalContributions: 0
  });

  useEffect(() => {
    fetchUsers();
    fetchStats();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('/api/admin/users');
      if (!response.ok) throw new Error('Failed to fetch users');
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/admin/stats');
      if (!response.ok) throw new Error('Failed to fetch stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold">Total Users</h2>
          <p className="text-3xl font-bold">{stats.totalUsers}</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold">Pro Users</h2>
          <p className="text-3xl font-bold">{stats.proUsers}</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold">Total Scans</h2>
          <p className="text-3xl font-bold">{stats.totalScans}</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold">Total Contributions</h2>
          <p className="text-3xl font-bold">{stats.totalContributions}</p>
        </div>
      </div>

      <h2 className="text-2xl font-semibold mb-4">User List</h2>
      <table className="w-full bg-white shadow rounded">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 text-left">Username</th>
            <th className="p-2 text-left">Tier</th>
            <th className="p-2 text-left">Daily Scans</th>
            <th className="p-2 text-left">Total Contributions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td className="p-2">{user.username}</td>
              <td className="p-2">{user.tier}</td>
              <td className="p-2">{user.dailyScans}</td>
              <td className="p-2">
                {Object.values(user.contributions).reduce((a, b) => a + b, 0)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboard;
