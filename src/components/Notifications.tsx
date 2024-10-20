import React, { useEffect, useState } from 'react';

interface NotificationsProps {
  rewards?: any[];
  dailyScans?: number;
}

const Notifications: React.FC<NotificationsProps> = ({ rewards = [], dailyScans = 0 }) => {
  const [notifications, setNotifications] = useState<string[]>([]);

  useEffect(() => {
    const checkNotifications = () => {
      const newNotifications = [];

      // Check daily scans
      if (dailyScans >= 5) {
        newNotifications.push("You've reached your daily scan limit!");
      }

      // Check rewards
      rewards.forEach(reward => {
        if (reward.status === 'new') {
          newNotifications.push(`You've earned a new reward: ${reward.type}`);
        }
      });

      setNotifications(newNotifications);
    };

    checkNotifications();
  }, [rewards, dailyScans]);

  return (
    <div className="bg-white shadow rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">Notifications</h2>
      {notifications.length > 0 ? (
        <ul>
          {notifications.map((notification, index) => (
            <li key={index} className="mb-2">{notification}</li>
          ))}
        </ul>
      ) : (
        <p>No new notifications</p>
      )}
    </div>
  );
};

export default Notifications;
