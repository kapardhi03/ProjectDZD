import React from 'react'

const Ddosslowloris = () => {
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
            <p>Upon examination of the network logs, it appears that the ongoing assault exhibits characteristics consistent with a DDoS (Distributed Denial of Service) Slowloris attack. Slowloris is a type of DDoS attack that targets web servers by utilizing a low-and-slow technique, where the attacker establishes multiple connections to the target server and sends partial HTTP requests, keeping those connections open for as long as possible.</p>
            <p>Slowloris DDoS attacks can cause significant disruption by exhausting server resources, occupying available connections, and rendering the web server unresponsive to legitimate user requests.
            To address this Slowloris DDoS attack effectively, it is recommended that we undertake the following actions:</p>

            <p>1. Implement DDoS Mitigation Services:</p>
            <div style={Style.intext}>
                <p>Engage with DDoS mitigation service providers to deploy specialized solutions capable of identifying and mitigating Slowloris attacks. These services employ techniques such as connection limits, traffic analysis, and behavioral monitoring to protect the targeted web server.</p>
            </div>
            <p>2. Configure Web Server Timeouts:</p>
            <div style={Style.intext}>
                <p>Adjust the web server's timeout settings to ensure that idle connections are closed within a reasonable time. By implementing shorter timeout values, the impact of Slowloris attacks can be minimized, as the attacker's partial requests will be terminated more quickly.</p>
            </div>
            <p>3. Utilize Connection Rate Limiting:</p>
            <div style={Style.intext}>
                <p>Implement connection rate limiting mechanisms on the server or load balancer to restrict the number of connections a single IP address or client can establish within a given time frame. This helps prevent the attacker from overwhelming the server with numerous slow connections.</p>
            </div>
            <p>4. Deploy Web Application Firewalls (WAFs):</p>
            <div style={Style.intext}>
                <p>Utilize WAFs to filter and block malicious Slowloris attack traffic targeting the web applications. WAFs can detect and mitigate the low-and-slow techniques employed by Slowloris, preventing them from consuming server resources and impacting the availability of the web server.</p>
            </div>
        </div >
    )
}

export default Ddosslowloris