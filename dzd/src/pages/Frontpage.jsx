import React, { useEffect, useState, useRef } from 'react';
import 'bootstrap/dist/css/bootstrap.css'; // Import Bootstrap CSS
import 'bootstrap/dist/js/bootstrap.bundle'; // Import Bootstrap JavaScript
import "./Nav.css";
// import instructions from './instructions';
const Navbar = () => {
  const [navbarVisible, setNavbarVisible] = useState(true);
  const [activeQuestion, setActiveQuestion] = useState(null);

  // ... (existing code)

  // const [activeQuestion, setActiveQuestion] = useState(null);

  const handleQuestionClick = (index) => {
    setActiveQuestion(index === activeQuestion ? null : index);
  };
  const [feedback, setFeedback] = useState('');
  const handleSubmitFeedback = (e) => {
    e.preventDefault();
    // Perform the necessary actions with the submitted feedback
    console.log('Submitted feedback:', feedback);
    // Reset the feedback state
    setFeedback('');
  };

  const faqRef = useRef(null);
  const feedbackRef = useRef(null);

  const handleWhatsAppShare = () => {
    const url = window.location.href;
    const encodedUrl = encodeURIComponent(url);
    const whatsappUrl = `https://api.whatsapp.com/send?text=${encodedUrl}`;
    window.open(whatsappUrl, '_blank');
  };

  const handleCopyLink = () => {
    const url = window.location.href;
    navigator.clipboard.writeText(url);
    alert('Link copied to clipboard!');
  };

  const handleQuestionClick2 = (questionId) => {
    setActiveQuestion(questionId === activeQuestion ? null : questionId);
  };

  const handleFaqClick = () => {
    if (faqRef.current) {
      faqRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };


  const handleFeedbackClick = () => {
    if (feedbackRef.current) {
      feedbackRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.pageYOffset;
      if (scrollPosition > 0) {
        setNavbarVisible(false);
      } else {
        setNavbarVisible(true);
      }
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);




  return (
    <div className='Body'>
      <section id='nav'>
        <nav className={`navbar navbar-expand-lg navbar-dark bg-dark fixed-top ${navbarVisible ? '' : 'navbar-hidden'}`}>
          <div className="container-fluid">
            <a className="navbar-brand" href="#">DZD</a>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent" aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarContent">
              <ul className="navbar-nav ms-auto me-3">
                <li className="nav-item">
                  <a className="nav-link active" aria-current="page" href="#">Home</a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" href="#">Sign Up</a>
                </li>
                <li className="nav-item dropdown">
                  <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    More
                  </a>
                  <ul className="dropdown-menu dropdown-menu-dark dropdown-menu-end">
                    <li><a className="dropdown-item" href="/Upload">Action</a></li>
                    <li><hr className="dropdown-divider" /></li>
                    <li><a className="dropdown-item" href="#" onClick={handleWhatsAppShare}>Share via WhatsApp</a></li>
                    <li><a className="dropdown-item" href="#" onClick={handleCopyLink}>Copy Link</a></li>
                    <li><hr className="dropdown-divider" /></li>
                    <a className="dropdown-item small-link" href="#feedback" onClick={handleFeedbackClick}>Feedback</a>
                    <a className="dropdown-item small-link" href="#faq" onClick={handleFaqClick}>FAQ</a>
                  </ul>
                </li>
              </ul>
            </div>
          </div>
        </nav>
      </section>

      <section id='part1'>
        <h1 className='Title'>Welcome to DetectiveZeroday</h1>
        <img className='FirstIMG' src='https://i.pinimg.com/564x/f1/f5/98/f1f59847fedb175f01f45dd7f3c16ccc.jpg' alt='Image' />
      </section>

      <section id='part2' style={{ padding: '0px 3% 0px 0%', borderRadius: '7%', width: '100%' }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '0.2%' }}>
          <div style={{ marginRight: '2%' }}>
            <img src='https://www.malwarebytes.com/blog/images/uploads/2020/06/zero-day-image.jpg' alt='Image' style={{ width: '500px', height: '400px', borderRadius: '10%', objectFit: 'cover' }} />
          </div>
          <div style={{ maxWidth: '550px' }}>
            <p className='para' style={{ textAlign: 'justify' }}>The term <a href='https://en.wikipedia.org/wiki/Zero-day_(computing)' style={{ color: '#007BFF', textDecoration: 'none' }}> "zero-day"</a> implies that both the vulnerability and the attack are discovered or disclosed on the same day, leaving no time for the software vendor to develop and release a patch to address the issue. This makes zero-day attacks particularly dangerous because they can be launched against systems that are unaware of the vulnerability, providing little or no time for defense measures. A zero-day attack refers to a cybersecurity vulnerability or exploit that is unknown to the software vendor or the public. It takes advantage of a security weakness that the software developer is unaware of, leaving users exposed to potential attacks.</p>
          </div>
        </div>
      </section>

      <section id='part3'>
        <div id="carouselExampleFade" class="carousel slide carousel-fade" data-bs-ride="carousel" data-bs-interval="3000">
          <div class="carousel-inner">
            <div class="carousel-item active">
              <img src="https://www.indusface.com/wp-content/uploads/2019/08/3-Ways-to-Prevent-Application-Zero-Day-Attacks.png" class="d-block w-100" alt="images" />
            </div>
            <div class="carousel-item">
              <img src="https://www.indusface.com/wp-content/uploads/2019/08/1-3.png" class="d-block w-100" alt="images" />
            </div>
            <div class="carousel-item">
              <img src="https://static.hindawi.com/articles/scn/volume-2021/6610675/figures/6610675.fig.003.jpg" class="d-block w-100" alt="images" />
            </div>
          </div>
          <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleFade" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="false"></span>
            <span class="visually-hidden">Previous</span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleFade" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="false"></span>
            <span class="visually-hidden">Next</span>
          </button>
        </div>
      </section>


      {/* FAQ */}
      <div className="container-small">
        <section ref={faqRef} className="hexagon cursor-default">
          <div className="hexagon-content">
            <h2 className='faq'>FAQ</h2>
            <p>
              <i >Find answers to frequently asked questions about Zeroday attacks:</i>
            </p>
            <ul>
              <li
                onClick={() => handleQuestionClick2(0)}
                className={activeQuestion === 0 ? 'active' : ''}
              >
                <h5>What is a Zeroday attack?</h5>
                {activeQuestion === 0 && (
                  <p className="Answers">
                    A Zeroday attack refers to a cybersecurity vulnerability or exploit
                    that is unknown to the software vendor or the public. It takes
                    advantage of a security weakness that the software developer is
                    unaware of, leaving users exposed to potential attacks.
                  </p>
                )}
              </li>
              <li
                onClick={() => handleQuestionClick2(1)}
                className={activeQuestion === 1 ? 'active' : ''}
              >
                <h5>How do Zeroday attacks occur?</h5>
                {activeQuestion === 1 && (
                  <p className="Answers">
                    Zeroday attacks typically occur when a hacker discovers a
                    vulnerability in software before the software developer or vendor
                    becomes aware of it. The attacker then exploits this vulnerability
                    to carry out malicious activities, such as gaining unauthorized
                    access, stealing data, or spreading malware.
                  </p>
                )}
              </li>
              <li
                onClick={() => handleQuestionClick2(2)}
                className={activeQuestion === 2 ? 'active' : ''}
              >
                <h5>What are the consequences of a Zeroday attack?</h5>
                {activeQuestion === 2 && (
                  <p className="Answers">
                    The consequences of a Zeroday attack can be severe. It can result
                    in data breaches, financial losses, damage to a company's
                    reputation, and disruption of critical services. Additionally,
                    Zeroday attacks can be challenging to detect and mitigate since
                    there is no prior knowledge of the vulnerability.
                  </p>
                )}
              </li>
              <li onClick={() => handleQuestionClick2(3)} className={activeQuestion === 3 ? 'active' : ''}>
                <h5>
                  How can organizations protect themselves against Zero-day attacks?
                  <span className="arrow"></span>
                </h5>
                {activeQuestion === 3 && (
                  <p className="Answers">
                    Organizations can take several measures to protect themselves against Zero-day attacks:
                    <ul>
                      <li>Regularly update software and apply security patches.</li>
                      <li>Implement robust network security measures, such as firewalls and intrusion detection systems.</li>
                      <li>Use behavior-based detection mechanisms to identify abnormal activities.</li>
                      <li>Implement multi-factor authentication to enhance access control.</li>
                      <li>Train employees on cybersecurity best practices and promote a security-conscious culture.</li>
                      <li>Partner with cybersecurity experts to conduct regular security assessments and audits.</li>
                    </ul>
                  </p>
                )}
              </li>

              <li onClick={() => handleQuestionClick2(4)} className={activeQuestion === 4 ? 'active' : ''}>
                <h5>
                  Are there any preventive measures for Zero-day attacks?
                  <span className="arrow"></span>
                </h5>
                {activeQuestion === 4 && (
                  <p className="Answers">
                    Preventing Zero-day attacks entirely is challenging due to their nature. However, organizations can take proactive measures to reduce the risk:
                    <ul>
                      <li>Implement a robust cybersecurity framework that includes regular vulnerability assessments and patch management.</li>
                      <li>Deploy advanced threat detection systems that utilize machine learning and behavioral analysis.</li>
                      <li>Practice defense-in-depth by implementing multiple layers of security controls.</li>
                      <li>Stay informed about the latest vulnerabilities and security advisories.</li>
                      <li>Establish incident response plans to mitigate the impact of a Zero-day attack.</li>
                    </ul>
                  </p>
                )}
              </li>

              <li
                onClick={() => handleQuestionClick2(5)}
                className={activeQuestion === 3 ? 'active' : ''}
              >
                <h5>How can I get my own Network Logs?</h5>
                {activeQuestion === 5 && (
                  <p className="Answers">
                    To get your own logs please follow these{' '}
                    <a className="logs" href="/instructions">
                      STEPS
                    </a>
                    .
                  </p>
                )}
              </li>
            </ul>
          </div>
        </section>

        <section ref={feedbackRef} className="hexagon">
          <div className="hexagon-content ">
            <h2>Feedback</h2>
            <p>
              Please provide your valuable feedback here
            </p>
            <form onSubmit={handleSubmitFeedback}>
              <textarea
                className="form-control feedback-textarea"
                placeholder="Enter your feedback"
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                required
              ></textarea>
              <button type="submit" className="btn btn-primary">Submit</button>
            </form>
          </div>
        </section>
      </div>

      <section id='final'>
        <a className="btn" target='_blank' href="mailto:kapardhikannekanti@gmail.com">CONTACT ME</a>
      </section>

      <div className="bottom-container">
        <div className="Link">
          <a className="footer-link" target='_blank' href="https://www.linkedin.com/in/kapardhi-kannekanti-a91a4325b">@LinkedIn</a>
          <span className="link-space"></span>
          <a className="footer-link" target='_blank' href="https://twitter.com/kapardhi200903">@Twitter</a>
          <span className="link-space"></span>
          <a className="footer-link" target='_blank' href="https://www.instagram.com/kapardhi.kannekanti/">@Instagram</a>
        </div>
        <p className="cpyryt">©kapardhikannekanti.</p>
      </div>
    </div>
  );
}
export default Navbar;
