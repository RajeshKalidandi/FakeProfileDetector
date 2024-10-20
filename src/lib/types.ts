interface User {
  // ... existing fields
  tier: 'free' | 'pro';
  dailyScans: number;
  lastReset: Date;
  contributions: {
    verifiedProfiles: number;
    validReports: number;
    feedbackCount: number;
  };
  rewards: {
    type: string;
    grantedAt: Date;
    expiresAt: Date;
    status: 'active' | 'expired';
  }[];
}
