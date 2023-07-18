import React from 'react';
import './AboutUs.css';
import { Link } from 'react-router-dom'; // Import the Link component

const AboutUs = () => {
  return (
    <div>
      
      <div className="about-container">
        
        <Link to="/" className="home-button">
          Home
        </Link>


        <div className="about-content">

          <h2 className="about-title">About DZD</h2>
          <p>
            Welcome to ZeroShield, a cutting-edge platform dedicated to providing comprehensive cybersecurity solutions. At
            ZeroShield, we are committed to safeguarding your digital assets and protecting you from emerging cyber threats.
          </p>

          <h3 className="about-subtitle">Our Mission</h3>
          <p>
            Our mission is to empower individuals, businesses, and organizations with advanced cybersecurity tools and knowledge
            to proactively defend against cyber attacks. We strive to create a secure online environment by leveraging innovative
            technologies and delivering top-notch security solutions.
          </p>

          <h3 className="about-subtitle">How We Work</h3>
          <p>
            At ZeroShield, we combine state-of-the-art technologies, threat intelligence, and expert analysis to detect and
            mitigate cyber threats effectively. Our dedicated team of cybersecurity professionals stays ahead of the evolving
            threat landscape, continuously improving our security measures and providing real-time protection against known and
            emerging threats.
          </p>

          <h3 className="about-subtitle">Our Features</h3>
          <ul>
            <li>
              <strong>Advanced Threat Detection:</strong> Our cutting-edge algorithms and machine learning techniques enable us
              to detect and prevent a wide range of cyber threats, including zero-day attacks.
            </li>
            <li>
              <strong>Real-Time Alerts:</strong> We deliver instant alerts and notifications whenever suspicious activities or
              potential security breaches are detected, allowing you to take immediate action.
            </li>
            <li>
              <strong>Comprehensive Reporting:</strong> Our detailed reports provide valuable insights into detected threats,
              their impact, and recommended mitigation strategies, helping you make informed decisions to enhance your security
              posture.
            </li>
            <li>
              <strong>User-Friendly Interface:</strong> Our intuitive and user-friendly interface simplifies the process of
              managing and monitoring your security systems, making it accessible for both cybersecurity experts and beginners.
            </li>
            <li>
              <strong>Customizable Settings:</strong> Tailor our security solutions to meet your specific requirements by
              adjusting settings and configurations based on your organization's needs and preferences.
            </li>
          </ul>

          <h3 className="about-subtitle">Our Commitment to Security</h3>
          <p>
            At ZeroShield, we prioritize the security and privacy of your data. We adhere to industry best practices and
            implement robust security measures to ensure the confidentiality, integrity, and availability of your sensitive
            information. Our infrastructure undergoes regular audits and updates to stay resilient against the evolving threat
            landscape.
          </p>

          <h3 className="about-subtitle">Get Started</h3>
          <p>
            Protect your digital assets with our cutting-edge cybersecurity solutions. Sign up today and experience peace of mind
            knowing that your online presence is fortified against cyber threats.
          </p>

          <div className="contact-info">
            <h3 className="about-subtitle">Contact Us</h3>
            <p>
              Have questions or need assistance? Our friendly support team is here to help. Reach out to us at{' '}
              <strong>[Contact Email : <a href="mailto:detectivezeroday@gmail.com">detectivezeroday@gmail.com</a>/Phone Number : 9848022338]</strong>, and we'll be happy to assist you.
            </p>
          </div>
        </div>

      </div>
      </div>
      );
};

      export default AboutUs;
