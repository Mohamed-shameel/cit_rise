import React, { useState, useEffect } from 'react';
import './AdminOpportunities.css';

const AdminOpportunitiesPanel = () => {
  const [opportunities, setOpportunities] = useState([]);
  const [syncLogs, setSyncLogs] = useState([]);
  const [deduplicationLogs, setDeduplicationLogs] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('opportunities');

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    domain: [],
    type: 'opportunity',
    company: '',
    location: 'India',
    source_url: '',
    deadline: '',
    salary_range: '',
    duration: ''
  });

  // Fetch data on mount
  useEffect(() => {
    fetchOpportunities();
    fetchSyncLogs();
    fetchDeduplicationLogs();
  }, []);

  const fetchOpportunities = async () => {
    try {
      const res = await fetch('http://localhost:8000/opportunities/admin/all');
      const data = await res.json();
      setOpportunities(data.opportunities || []);
    } catch (error) {
      console.error('Failed to fetch opportunities:', error);
    }
  };

  const fetchSyncLogs = async () => {
    try {
      const res = await fetch('http://localhost:8000/opportunities/admin/sync-logs');
      const data = await res.json();
      setSyncLogs(data.logs || []);
    } catch (error) {
      console.error('Failed to fetch sync logs:', error);
    }
  };

  const fetchDeduplicationLogs = async () => {
    try {
      const res = await fetch('http://localhost:8000/opportunities/admin/deduplication-logs');
      const data = await res.json();
      setDeduplicationLogs(data.logs || []);
    } catch (error) {
      console.error('Failed to fetch dedup logs:', error);
    }
  };

  const handleSyncUnstop = async () => {
    try {
      setLoading(true);
      const res = await fetch('http://localhost:8000/opportunities/admin/sync-unstop', {
        method: 'POST'
      });
      const data = await res.json();

      if (res.ok) {
        alert(`✅ Sync completed!\nAdded: ${data.added}\nDuplicates merged: ${data.duplicates}`);
        fetchOpportunities();
        fetchSyncLogs();
        fetchDeduplicationLogs();
      } else {
        alert(`❌ Sync failed: ${data.detail}`);
      }
    } catch (error) {
      console.error('Sync error:', error);
      alert('Sync failed');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateOpportunity = async (e) => {
    e.preventDefault();

    if (!formData.title || !formData.company || !formData.source_url) {
      alert('Please fill in Title, Company, and Source URL');
      return;
    }

    try {
      setLoading(true);
      const res = await fetch('http://localhost:8000/opportunities/admin/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          domain: formData.domain.split(',').map(d => d.trim()).filter(d => d)
        })
      });

      const data = await res.json();

      if (res.ok) {
        alert('✅ Opportunity created successfully!');
        setFormData({
          title: '',
          description: '',
          domain: [],
          type: 'opportunity',
          company: '',
          location: 'India',
          source_url: '',
          deadline: '',
          salary_range: '',
          duration: ''
        });
        setShowCreateForm(false);
        fetchOpportunities();
      } else {
        alert(`❌ Error: ${data.detail}`);
      }
    } catch (error) {
      console.error('Create error:', error);
      alert('Failed to create opportunity');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteOpportunity = async (oppId) => {
    if (!window.confirm('Are you sure you want to delete this opportunity?')) return;

    try {
      const res = await fetch(`http://localhost:8000/opportunities/admin/${oppId}`, {
        method: 'DELETE'
      });

      if (res.ok) {
        alert('✅ Opportunity deleted');
        fetchOpportunities();
      } else {
        alert('❌ Failed to delete');
      }
    } catch (error) {
      console.error('Delete error:', error);
    }
  };

  const handleVerifyOpportunity = async (oppId) => {
    try {
      const res = await fetch(`http://localhost:8000/opportunities/admin/${oppId}/verify`, {
        method: 'PUT'
      });

      if (res.ok) {
        alert('✅ Opportunity verified');
        fetchOpportunities();
      } else {
        alert('❌ Failed to verify');
      }
    } catch (error) {
      console.error('Verify error:', error);
    }
  };

  const tabbedOpportunities = opportunities.filter(o =>
    activeTab === 'all' || (activeTab === 'verified' && o.verified) || (activeTab === 'unverified' && !o.verified)
  );

  return (
    <div className="admin-opps-panel">
      <div className="admin-header">
        <h1>🔧 Opportunities Management</h1>
        <p>Create, verify, and sync opportunities</p>
      </div>

      <div className="admin-toolbar">
        <button
          className="btn-action btn-sync"
          onClick={handleSyncUnstop}
          disabled={loading}
        >
          {loading ? '⏳ Syncing...' : '🔄 Sync Unstop'}
        </button>
        <button
          className="btn-action btn-create"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? '✕ Cancel' : '➕ Create New Opportunity'}
        </button>
      </div>

      {showCreateForm && (
        <div className="create-form-container">
          <h2>Create New Opportunity</h2>
          <form onSubmit={handleCreateOpportunity} className="create-form">
            <div className="form-row">
              <input
                type="text"
                placeholder="Title"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                required
              />
              <input
                type="text"
                placeholder="Company"
                value={formData.company}
                onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                required
              />
            </div>

            <textarea
              placeholder="Description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows="3"
            />

            <div className="form-row">
              <select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              >
                <option value="opportunity">Opportunity</option>
                <option value="internship">Internship</option>
                <option value="competition">Competition</option>
                <option value="research">Research</option>
                <option value="job">Job</option>
                <option value="workshop">Workshop</option>
                <option value="fellowship">Fellowship</option>
              </select>
              <input
                type="text"
                placeholder="Domains (comma-separated, e.g. AI/ML, Startup)"
                value={formData.domain}
                onChange={(e) => setFormData({ ...formData, domain: e.target.value })}
              />
            </div>

            <div className="form-row">
              <input
                type="url"
                placeholder="Source URL (required)"
                value={formData.source_url}
                onChange={(e) => setFormData({ ...formData, source_url: e.target.value })}
                required
              />
              <input
                type="text"
                placeholder="Location"
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              />
            </div>

            <div className="form-row">
              <input
                type="date"
                placeholder="Deadline"
                value={formData.deadline}
                onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
              />
              <input
                type="text"
                placeholder="Salary Range"
                value={formData.salary_range}
                onChange={(e) => setFormData({ ...formData, salary_range: e.target.value })}
              />
              <input
                type="text"
                placeholder="Duration"
                value={formData.duration}
                onChange={(e) => setFormData({ ...formData, duration: e.target.value })}
              />
            </div>

            <button type="submit" className="btn-submit" disabled={loading}>
              {loading ? 'Creating...' : 'Create Opportunity'}
            </button>
          </form>
        </div>
      )}

      <div className="admin-tabs">
        <button
          className={`tab ${activeTab === 'opportunities' ? 'active' : ''}`}
          onClick={() => setActiveTab('opportunities')}
        >
          📋 All Opportunities ({opportunities.length})
        </button>
        <button
          className={`tab ${activeTab === 'logs' ? 'active' : ''}`}
          onClick={() => setActiveTab('logs')}
        >
          📊 Sync & Dedup Logs
        </button>
      </div>

      {activeTab === 'opportunities' && (
        <div className="opportunities-list">
          <div className="filter-tabs">
            <button
              className={`filter-tab ${activeTab === 'all' ? 'active' : ''}`}
              onClick={() => setActiveTab('all')}
            >
              All ({opportunities.length})
            </button>
            <button
              className={`filter-tab ${activeTab === 'verified' ? 'active' : ''}`}
              onClick={() => setActiveTab('verified')}
            >
              ✓ Verified ({opportunities.filter(o => o.verified).length})
            </button>
            <button
              className={`filter-tab ${activeTab === 'unverified' ? 'active' : ''}`}
              onClick={() => setActiveTab('unverified')}
            >
              ⚠ Unverified ({opportunities.filter(o => !o.verified).length})
            </button>
          </div>

          <div className="opp-admin-grid">
            {tabbedOpportunities.map(opp => (
              <div key={opp.opportunity_id} className="admin-opp-card">
                <div className="admin-opp-header">
                  <h3>{opp.title}</h3>
                  <span className={`verified-badge ${opp.verified ? 'verified' : 'unverified'}`}>
                    {opp.verified ? '✓ Verified' : '⚠ Pending Verification'}
                  </span>
                </div>

                <p className="company">{opp.company}</p>
                <p className="source">Source: {opp.source}</p>

                {opp.department_fit && opp.department_fit.length > 0 && (
                  <div className="dept-fit">
                    <strong>Fit for:</strong> {opp.department_fit.join(', ')}
                  </div>
                )}

                {opp.ai_analysis && (
                  <div className="ai-analysis">
                    <p>Score: {opp.ai_analysis.relevance_score}/10</p>
                    <p>Difficulty: {opp.ai_analysis.difficulty_level}</p>
                  </div>
                )}

                <div className="admin-actions">
                  <a
                    href={opp.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-view"
                  >
                    View
                  </a>
                  {!opp.verified && opp.source === 'admin' && (
                    <button
                      className="btn-verify"
                      onClick={() => handleVerifyOpportunity(opp.opportunity_id)}
                    >
                      Verify
                    </button>
                  )}
                  <button
                    className="btn-delete"
                    onClick={() => handleDeleteOpportunity(opp.opportunity_id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'logs' && (
        <div className="logs-section">
          <div className="log-container">
            <h3>🔄 Sync Logs</h3>
            <div className="log-list">
              {syncLogs.length === 0 ? (
                <p className="no-logs">No sync logs yet</p>
              ) : (
                syncLogs.map(log => (
                  <div key={log.sync_id} className="log-item">
                    <p className="sync-time">{new Date(log.timestamp).toLocaleString()}</p>
                    <p>Added: <strong>{log.added}</strong> | Duplicates: <strong>{log.duplicates}</strong></p>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="log-container">
            <h3>🔀 Deduplication Logs</h3>
            <div className="log-list">
              {deduplicationLogs.length === 0 ? (
                <p className="no-logs">No deduplication events yet</p>
              ) : (
                deduplicationLogs.map(log => (
                  <div key={log.merge_id} className="log-item">
                    <p className="merge-time">{new Date(log.merged_at).toLocaleString()}</p>
                    <p>Merged into: <strong>{log.primary_opp_id}</strong></p>
                    <p className="merge-reason">{log.reason}</p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminOpportunitiesPanel;
