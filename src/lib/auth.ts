import { auth } from '../firebase';
import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut, 
  User as FirebaseUser 
} from 'firebase/auth';
import { getFirestore, doc, setDoc } from 'firebase/firestore';

const db = getFirestore();

export const register = async (username: string, email: string, password: string): Promise<FirebaseUser> => {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
  const user = userCredential.user;

  // Store additional user info in Firestore
  await setDoc(doc(db, 'users', user.uid), {
    username: username,
    email: email,
    createdAt: new Date(),
    tier: 'free',
    dailyScans: 0,
    lastReset: new Date(),
    contributions: {
      verifiedProfiles: 0,
      validReports: 0,
      feedbackCount: 0,
      totalPoints: 0
    },
    rewards: []
  });

  return user;
};

export const login = async (email: string, password: string): Promise<FirebaseUser> => {
  const userCredential = await signInWithEmailAndPassword(auth, email, password);
  return userCredential.user;
};

export const logout = (): Promise<void> => {
  return signOut(auth);
};

export const getCurrentUser = (): FirebaseUser | null => {
  return auth.currentUser;
};

export const getIdToken = async (): Promise<string | null> => {
  const user = auth.currentUser;
  if (user) {
    return user.getIdToken();
  }
  return null;
};
