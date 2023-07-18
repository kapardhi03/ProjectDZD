    import React from 'react'

    const Sshpatator = () => {
        const Style = {
            text: {
                margin: '2em',
                color: '#444141',
                fontFamily: 'Inter, sans-serif',
                fontSize: '16px',
                fontWeight: 'bold',
                textAlign: 'left'
                
            },
            intext: {
                // fontWeight: 'normal',
                marginLeft: '2em',
                marginRight: '1 em',
                marginBottom: '1em',
                justifyContent:'flex-start',
                display : 'flex',
                textAlign: 'left'
            }
        };

        return (
            <div style={Style.text}>
                <p>Upon examination of the network logs, it appears that there is evidence of an SSH (Secure Shell) Patator attack. SSH Patator is a type of brute-force attack that targets SSH servers by systematically attempting various username and password combinations until a successful login is achieved.</p>
                <p>SSH Patator attacks can pose a significant security risk as they exploit weak or default SSH credentials, potentially gaining unauthorized access to the SSH server and compromising the system.
                    To address this SSH Patator attack effectively, it is recommended that we undertake the following actions:</p>

                <p>1. Implement Strong Authentication Measures:</p>
                <div style={Style.intext}>
                    <p>Ensure that strong and unique usernames and passwords are enforced for SSH server access. Implement password policies that require a combination of uppercase and lowercase letters, numbers, and special characters to mitigate the risk of brute-force attacks.</p>
                </div>
                <p>2. Implement Intrusion Detection and Prevention Systems:</p>
                <div style={Style.intext}>
                    <p>Deploy intrusion detection and prevention systems that can monitor SSH server traffic and detect suspicious login patterns indicative of SSH Patator attacks. These systems can automatically block or alert administrators about such malicious activities.</p>
                </div>
                <p>3. Regularly Update and Patch SSH Software:</p>
                <div style={Style.intext}>
                    <p>Ensure that the SSH server software is kept up to date with the latest security patches and updates. This helps protect against known vulnerabilities that could be exploited during SSH Patator attacks.</p>
                </div>
                <p>4. Monitor and Analyze SSH Server Logs:</p>
                <div style={Style.intext}>
                    <p>Regularly review and analyze SSH server logs to identify any unusual login attempts or patterns. This can help identify ongoing SSH Patator attacks and allow for timely mitigation measures.</p>
                </div>
            </div >
        )
    }

    export default Sshpatator