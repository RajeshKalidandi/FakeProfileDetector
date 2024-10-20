import { User } from './types';

export class FreemiumService {
  private static DAILY_SCAN_LIMIT = 10;

  static async checkScanLimit(user: User): Promise<boolean> {
    if (!user) throw new Error('User not found');

    if (user.tier === 'pro') return true;
    
    const today = new Date();
    if (user.lastReset.getDate() !== today.getDate()) {
      user.dailyScans = 0;
      user.lastReset = today;
      await this.updateUser(user);
    }

    return user.dailyScans < this.DAILY_SCAN_LIMIT;
  }

  static async incrementScanCount(user: User): Promise<void> {
    if (!user) throw new Error('User not found');

    user.dailyScans++;
    if (user.dailyScans > this.DAILY_SCAN_LIMIT) {
      throw new Error('Daily scan limit exceeded');
    }
    await this.updateUser(user);
  }

  static async addContribution(user: User, type: 'verifiedProfiles' | 'validReports' | 'feedbackCount'): Promise<void> {
    if (!user) throw new Error('User not found');
    if (!user.contributions[type]) throw new Error('Invalid contribution type');

    user.contributions[type]++;
    await this.checkRewards(user);
    await this.updateUser(user);
  }

  private static async checkRewards(user: User): Promise<void> {
    if (user.contributions.verifiedProfiles >= 50) {
      await this.grantReward(user, 'UNLIMITED_SCANNING', '7d');
    }
    if (user.contributions.validReports >= 10) {
      await this.grantReward(user, 'ADVANCED_ML', '3d');
    }
    if (user.contributions.feedbackCount >= 30) {
      await this.grantReward(user, 'BULK_UPGRADE', '2d');
    }
  }

  static async grantReward(user: User, rewardType: string, duration: string): Promise<void> {
    if (!user) throw new Error('User not found');

    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + parseInt(duration));
    
    user.rewards.push({
      type: rewardType,
      grantedAt: new Date(),
      expiresAt,
      status: 'active'
    });
    await this.updateUser(user);
  }

  private static async updateUser(user: User): Promise<void> {
    // Implement user update logic (e.g., API call to backend)
    try {
      const response = await fetch(`/api/users/${user.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user)
      });
      if (!response.ok) throw new Error('Failed to update user');
    } catch (error) {
      console.error('Error updating user:', error);
      throw error;
    }
  }
}
