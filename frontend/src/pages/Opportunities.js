import React, { useState, useEffect } from 'react';
import './Opportunities.css';

const OpportunitiesPage = ({ userId }) => {
  const [opportunities, setOpportunities] = useState([]);
  const [userOpportunities, setUserOpportunities] = useState([]);
  const [activeTab, setActiveTab] = useState('All');
  const [sortBy, setSortBy] = useState('deadline');
  const [loading, setLoading] = useState(false);
  const [selectedDept, setSelectedDept] = useState(null);

  const tabs = ['All', 'Internship', 'Competition', 'Research', 'Job', 'Workshop'];

  // Fetch opportunities
  useEffect(() => {
    fetchOpportunities();
    if (userId) fetchUserOpportunities();
  }, [userId, activeTab, sortBy]);

  const fetchOpportunities = async () => {
    try {
      setLoading(true);
      const type = activeTab !== 'All' ? activeTab.toLowerCase() : null;
      const params = new URLSearchParams();
      if (type) params.append('type', type);
      params.append('sort_by', sortBy);

      const res = await fetch(`http://localhost:8000/opportunities/?${params}`);
      const data = await res.json();
      setOpportunities(data.opportunities || []);
    } catch (error) {
      console.error('Failed to fetch opportunities:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUserOpportunities = async () => {
    try {
      const res = await fetch(`http://localhost:8000/opportunities/user/${userId}`);
      const data = await res.json();
      setUserOpportunities(data.opportunities || []);
    } catch (error) {
      console.error('Failed to fetch user opportunities:', error);
    }
  };

  const registerForOpportunity = async (oppId) => {
    try {
      const res = await fetch(`http://localhost:8000/opportunities/${oppId}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId })
      });

      if (res.ok) {
        alert('✅ Successfully registered for this opportunity!');
        fetchUserOpportunities();
      } else {
        const errorData = await res.json();
        alert(`❌ ${errorData.detail}`);
      }
    } catch (error) {
      console.error('Registration failed:', error);
    }
  };

  const isRegistered = (oppId) => {
    return userOpportunities.some(uo => uo.opportunity.opportunity_id === oppId);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'No deadline';
    const date = new Date(dateString);
    const today = new Date();
    const daysLeft = Math.ceil((date - today) / (1000 * 60 * 60 * 24));

    if (daysLeft < 0) return '❌ Expired';
    if (daysLeft === 0) return '⏰ Today';
    if (daysLeft === 1) return '⏰ Tomorrow';
    if (daysLeft <= 7) return `⏰ ${daysLeft} days left`;
    return date.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' });
  };

  const OpportunityCard = ({ opp }) => {
    const registered = isRegistered(opp.opportunity_id);
    const relevanceScore = opp.ai_analysis?.relevance_score || 5;
    const sourceColor = {
      'unstop': '#6366f1',
      'admin': '#f97316',
      'linkedin': '#0a66c2'
    }[opp.source] || '#666';

    return (
      <div className="opp-card">
        <div className="opp-header">
          <div className="opp-title-section">
            <h3>{opp.title}</h3>
            <div className="opp-badges">
              <span className="badge-type">{opp.type}</span>
              <span className="badge-source" style={{ backgroundColor: sourceColor }}>
                {opp.source}
              </span>
              {opp.verified && <span className="badge-verified">✓ Verified</span>}
            </div>
          </div>
          <div className="relevance-score">{relevanceScore}/10</div>
        </div>

        <div className="opp-meta">
          <p className="company">{opp.company}</p>
          <p className="location">{opp.location}</p>
          {opp.salary_range && <p className="salary">💰 {opp.salary_range}</p>}
        </div>

        <p className="description">{opp.description}</p>

        <div className="opp-domains">
          {opp.domain && opp.domain.map((d, i) => (
            <span key={i} className="domain-tag">{d}</span>
          ))}
        </div>

        <div className="opp-fit">
          <div className="fit-item">
            <span className="fit-label">Difficulty:</span>
            <span className="fit-value">{opp.ai_analysis?.difficulty_level || 'Medium'}</span>
          </div>
          <div className="fit-item">
            <span className="fit-label">Learning Value:</span>
            <span className="fit-value">{opp.ai_analysis?.learning_value || 'Medium'}</span>
          </div>
        </div>

        <div className="opp-footer">
          <div className="deadline">{formatDate(opp.deadline)}</div>
          <div className="actions">
            <a
              href={opp.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-view"
            >
              View on {opp.source === 'unstop' ? 'Unstop' : 'Site'} →
            </a>
            <button
              className={`btn-register ${registered ? 'registered' : ''}`}
              onClick={() => registerForOpportunity(opp.opportunity_id)}
              disabled={registered}
            >
              {registered ? '✓ Registered' : '✚ Register'}
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="opportunities-page">
      <div className="opp-header-section">
        <h1>🚀 Opportunities</h1>
        <p>Internships, Hackathons, Research, and more tailored to your profile</p>
      </div>

      <div className="opp-controls">
        <div className="tab-group">
          {tabs.map(tab => (
            <button
              key={tab}
              className={`tab ${activeTab === tab ? 'active' : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="sort-group">
          <label>Sort by:</label>
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
            <option value="deadline">Deadline (Soon First)</option>
            <option value="recently_added">Recently Added</option>
            <option value="relevance">Relevance Score</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading opportunities...</div>
      ) : opportunities.length === 0 ? (
        <div className="empty-state">
          <p>No opportunities found in this category</p>
          <p className="hint">Try switching tabs or check back soon!</p>
        </div>
      ) : (
        <div className="opp-grid">
          {opportunities.map(opp => (
            <OpportunityCard key={opp.opportunity_id} opp={opp} />
          ))}
        </div>
      )}

      {userOpportunities.length > 0 && (
        <div className="registered-section">
          <h2>📌 Your Active Registrations</h2>
          <div className="registered-grid">
            {userOpportunities.map(uo => (
              <div key={uo.registration.user_opp_id} className="registered-card">
                <h4>{uo.opportunity.title}</h4>
                <p className="company">{uo.opportunity.company}</p>
                <p className={`status status-${uo.registration.status}`}>
                  Status: {uo.registration.status}
                </p>
                <p className="registered-date">
                  Registered: {new Date(uo.registration.registered_at).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default OpportunitiesPage;
