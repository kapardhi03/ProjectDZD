import React from 'react'

const Infiltration = () => {
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
            <p>Upon examination of the network logs, it appears that there is evidence of an infiltration attempt into the system. Infiltration refers to the unauthorized entry into a network, system, or infrastructure with the intention of gaining access to sensitive information, compromising security, or carrying out malicious activities.
            To address this infiltration attempt effectively, it is recommended that we undertake the following actions:</p>

            <p>1. Activate Incident Response Plan:</p>
            <div style={Style.intext}>
                <p>Immediately activate the predefined incident response plan to ensure a coordinated and structured approach towards mitigating the infiltration and minimizing its impact. This includes notifying relevant stakeholders, isolating affected systems, and preserving evidence for forensic analysis.</p>
            </div>
            <p>2. Patch Vulnerabilities:</p>
            <div style={Style.intext}>
                <p>Identify and address any known vulnerabilities that could have been exploited during the infiltration attempt. This includes applying necessary security patches, updating software and firmware, and implementing security best practices.</p>
            </div>
            <p>3. Strengthen Access Controls:</p>
            <div style={Style.intext}>
                <p>Review and enhance access controls, including user accounts, privileges, and permissions. Implement strong authentication mechanisms, such as multi-factor authentication, and regularly review and revoke access for inactive or compromised accounts.</p>
            </div>
            <p>4. Monitor System Activity:</p>
            <div style={Style.intext}>
                <p>Implement robust system monitoring and log analysis to detect any suspicious activity and potential indicators of further infiltration attempts. Monitor network traffic, system behavior, and user activity to identify anomalies and promptly respond to any security incidents.</p>
            </div>
        </div >
    )
}

export default Infiltration