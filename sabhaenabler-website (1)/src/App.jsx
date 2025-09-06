import React from 'react';
import { Button } from '@/components/ui/button.jsx'
import './App.css'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>SabhaEnabler: Your Local Service Connection</h1>
        <p>Connecting neighbors with trusted local service providers, effortlessly.</p>
      </header>

      <section className="App-section">
        <h2>How It Works</h2>
        <div className="features-grid">
          <div className="feature-item">
            <h3>1. Customer Needs</h3>
            <p>Neighbors post their service requests (e.g., TV mounting, home repairs) on our platform.</p>
          </div>
          <div className="feature-item">
            <h3>2. Automated Matching</h3>
            <p>Our smart system instantly connects requests with qualified local service providers in our network.</p>
          </div>
          <div className="feature-item">
            <h3>3. Transparent Quotes</h3>
            <p>Providers submit quotes directly through the platform, which you can review and accept.</p>
          </div>
          <div className="feature-item">
            <h3>4. Seamless Service</h3>
            <p>Once accepted, the service is performed, and secure payments are processed through SabhaEnabler.</p>
          </div>
        </div>
      </section>

      <section className="App-section">
        <h2>Benefits for Customers</h2>
        <ul>
          <li>Find trusted local service providers quickly and easily.</li>
          <li>Receive multiple quotes to compare and choose the best option.</li>
          <li>Secure and transparent payment processing.</li>
          <li>Read reviews and ratings from other neighbors.</li>
        </ul>
      </section>

      <section className="App-section">
        <h2>Benefits for Service Providers</h2>
        <ul>
          <li>Access a steady stream of local job opportunities.</li>
          <li>Reduce marketing efforts and costs.</li>
          <li>Streamlined communication and booking management.</li>
          <li>Secure and timely payouts for completed jobs.</li>
          <li>Build your reputation with customer reviews.</li>
        </ul>
      </section>

      <section className="App-section call-to-action">
        <h2>Ready to Get Started?</h2>
        <p>Whether you need a service or offer one, SabhaEnabler is your go-to platform.</p>
        <div className="cta-buttons">
          <Button className="primary">I Need a Service</Button>
          <Button className="secondary">I Offer a Service</Button>
        </div>
      </section>

      <footer className="App-footer">
        <p>&copy; 2025 SabhaEnabler. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default App
