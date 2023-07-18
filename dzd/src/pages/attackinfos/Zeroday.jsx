import React from 'react'

const Zeroday = () => {
    const Style = {
        text: {
            margin: '2em',
            color: '#444141',
            fontFamily: 'Inter, sans-serif',
            fontSize: '16px',
            fontWeight: 'bold'   
        },
        intext: {
            // fontWeight: 'normal',
            marginLeft: '2em',
            marginRight: '1 em',
            marginBottom: '1em'
        }
    };

    return (
        <div style={Style.text}>
            <p>Upon examination of the network logs, it appears that the ongoing assault does not exhibit characteristics consistent with any previously documented attacks. Consequently, it is plausible that we are dealing with a potential zero-day attack, which warrants our immediate attention and concern.</p>

            {/* <p>A zero-day attack refers to a cybersecurity incident in which malicious actors exploit vulnerabilities in software or systems that are unknown to the software developers or security community. These vulnerabilities have not been addressed through official patches or updates, hence the term "zero-day," signifying zero days since the vulnerability was discovered.</p> */}
            <p>In such scenarios, attackers gain an advantage as they leverage undisclosed vulnerabilities, allowing them to breach security defenses undetected, manipulate systems, and potentially extract sensitive data or cause other detrimental consequences.</p>
            <p>To address this potential zero-day attack effectively, it is recommended that we undertake the following actions:</p>
            <br></br>
            <p>1. Initiate an Incident Response Plan:</p>
            <div style={Style.intext}>
            <p >Immediately activate our predefined incident response plan to ensure a coordinated and structured approach towards mitigating the attack and minimizing its impact.</p>
            </div>
            <p>2. Conduct In-Depth Investigations:</p>
            <div style={Style.intext}>
            <p >Engage specialized resources to perform detailed investigations and analysis to identify the nature and scope of the attack. This includes examining network logs, system behavior, and any other relevant sources of information.</p>
            </div>
            <p>3. Engage Security Experts:</p>
            <div style={Style.intext}>
            <p >Seek assistance from cybersecurity professionals or consultants with expertise in handling zero-day attacks. Their specialized knowledge and experience can aid in identifying and mitigating the specific vulnerabilities being exploited.</p>
            </div>
            <p>4. Monitor and Analyze Attack Patterns:</p>
            <div style={Style.intext}>
            <p >Continuously monitor network traffic and system behavior to identify any patterns or indicators that could shed light on the attack methodology. This information can help refine the incident response and enhance future prevention measures.</p>
        </div>
            </div >
    )
}

export default Zeroday