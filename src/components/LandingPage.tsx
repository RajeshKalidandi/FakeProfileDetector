import React from 'react';
import { motion } from 'framer-motion';
import { Shield, CheckCircle, AlertTriangle, Zap, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { FaFacebookF, FaTwitter, FaInstagram, FaLinkedinIn, FaTiktok } from 'react-icons/fa';

const LandingPage: React.FC = () => {
  const features = [
    { icon: Shield, title: 'Advanced AI', description: 'Cutting-edge algorithms for accurate detection of fake profiles' },
    { icon: CheckCircle, title: 'High Accuracy', description: '99% success rate in identifying and flagging suspicious accounts' },
    { icon: AlertTriangle, title: 'Instant Alerts', description: 'Real-time notifications for immediate action on potential threats' },
    { icon: Zap, title: 'Fast Analysis', description: 'Rapid profile scanning and results in seconds, not minutes' },
  ];

  const stats = [
    { value: '99%', label: 'Detection Accuracy' },
    { value: '1M+', label: 'Profiles Analyzed' },
    { value: '24/7', label: 'Expert Support' },
  ];

  const socialIcons = [
    { Icon: FaFacebookF, link: 'https://facebook.com' },
    { Icon: FaTwitter, link: 'https://twitter.com' },
    { Icon: FaInstagram, link: 'https://instagram.com' },
    { Icon: FaLinkedinIn, link: 'https://linkedin.com' },
    { Icon: FaTiktok, link: 'https://tiktok.com' },
  ];

  return (
    <div className="container mx-auto px-4 py-12">
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-16"
      >
        <h1 className="font-heading text-5xl font-bold mb-6 text-primary">
          Safeguard Your Online Presence with AI-Powered Fake Profile Detection
        </h1>
        <p className="text-xl mb-8 max-w-2xl mx-auto">
          Protect yourself and your community from fraudulent accounts. Our advanced AI technology detects fake profiles with 99% accuracy, ensuring a safer social media experience.
        </p>
        <Link
          to="/dashboard"
          className="bg-primary text-white font-semibold py-3 px-6 rounded-full hover:bg-blue-600 transition duration-300 inline-flex items-center"
        >
          Start Protecting Now <ArrowRight className="ml-2" />
        </Link>
      </motion.section>

      <section className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
        {features.map((feature, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition duration-300"
          >
            <feature.icon className="w-12 h-12 text-primary mb-4" />
            <h3 className="font-heading text-xl font-semibold mb-2">{feature.title}</h3>
            <p className="text-gray-600">{feature.description}</p>
          </motion.div>
        ))}
      </section>

      <section className="text-center mb-16">
        <h2 className="font-heading text-3xl font-bold mb-8">Trusted by Experts Worldwide</h2>
        <div className="flex flex-wrap justify-center gap-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="bg-white p-6 rounded-lg shadow-md"
            >
              <p className="text-4xl font-bold text-primary mb-2">{stat.value}</p>
              <p className="text-gray-600">{stat.label}</p>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="text-center mb-16">
        <h2 className="font-heading text-3xl font-bold mb-6">Why Choose Our Fake Profile Detector?</h2>
        <ul className="text-left max-w-2xl mx-auto">
          <li className="mb-4 flex items-start">
            <CheckCircle className="text-primary mr-2 flex-shrink-0 mt-1" />
            <span>Protect your personal information from scammers and identity thieves</span>
          </li>
          <li className="mb-4 flex items-start">
            <CheckCircle className="text-primary mr-2 flex-shrink-0 mt-1" />
            <span>Maintain the integrity of your social media community</span>
          </li>
          <li className="mb-4 flex items-start">
            <CheckCircle className="text-primary mr-2 flex-shrink-0 mt-1" />
            <span>Save time and resources by automating profile verification</span>
          </li>
          <li className="flex items-start">
            <CheckCircle className="text-primary mr-2 flex-shrink-0 mt-1" />
            <span>Stay ahead of evolving online threats with our constantly updated AI</span>
          </li>
        </ul>
      </section>

      <section className="text-center">
        <h2 className="font-heading text-3xl font-bold mb-6">Connect With Us</h2>
        <p className="mb-6 text-gray-600">Stay updated on the latest in online safety and fake profile detection</p>
        <div className="flex justify-center space-x-6">
          {socialIcons.map(({ Icon, link }, index) => (
            <motion.a
              key={index}
              href={link}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white p-3 rounded-full shadow-md hover:shadow-lg transition duration-300"
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              <Icon className="w-6 h-6 text-primary" />
            </motion.a>
          ))}
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
