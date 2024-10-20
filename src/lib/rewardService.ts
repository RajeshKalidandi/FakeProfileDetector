import { User } from './types';

export class RewardService {
  static async checkAndUpdateRewards(user: User): Promise<void> {
    const now = new Date();
    let updated = false;

    user.rewards = user.rewards.map(reward => {
      if (reward.status === 'active' && reward.expiresAt <= now) {
        reward.status = 'expired';
        updated = true;
      }
      return reward;
    });

    if (updated) {
      // Update user in the database
      try {
        const response = await fetch(`/api/users/${user.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(user)
        });
        if (!response.ok) throw new Error('Failed to update user rewards');
      } catch (error) {
        console.error('Error updating user rewards:', error);
        throw error;
      }
    }
  }
}
