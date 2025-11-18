import { useCallback, useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import './App.css';

ChartJS.register(ArcElement, Tooltip, Legend);

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';

const API_HOST = API_BASE_URL.replace(/\/+$/, '').replace(/\/api$/, '');

function App() {
  const [credentials, setCredentials] = useState({
    username: '',
    password: '',
  });
  const [selectedFile, setSelectedFile] = useState(null);
  const [latestSummary, setLatestSummary] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const authConfig = useMemo(() => {
    if (!credentials.username || !credentials.password) {
      return null;
    }
    return {
      auth: {
        username: credentials.username,
        password: credentials.password,
      },
    };
  }, [credentials]);

  const fetchHistory = useCallback(async () => {
    if (!authConfig) {
      return;
    }
    try {
      const response = await axios.get(`${API_BASE_URL}/history/`, authConfig);
      setHistory(response.data || []);
      setLatestSummary(response.data?.[0] || null);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to fetch history. Check your credentials and server.'
      );
    }
  }, [authConfig]);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!authConfig) {
      setError('Enter username & password to authenticate.');
      return;
    }
    if (!selectedFile) {
      setError('Please choose a CSV file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      setLoading(true);
      setError('');
      const response = await axios.post(`${API_BASE_URL}/upload/`, formData, {
        ...authConfig,
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setLatestSummary(response.data.dataset);
      await fetchHistory();
      setSelectedFile(null);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          'Upload failed. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const chartData = useMemo(() => {
    const distribution = latestSummary?.type_distribution || {};
    const labels = Object.keys(distribution);
    const values = Object.values(distribution);
    return {
      labels,
      datasets: [
        {
          label: 'Equipment Types',
          data: values,
          backgroundColor: [
            '#2563eb',
            '#ea580c',
            '#16a34a',
            '#f97316',
            '#a855f7',
            '#0ea5e9',
          ],
          borderWidth: 1,
        },
      ],
    };
  }, [latestSummary]);

  return (
    <div className="app-shell">
      <header>
        <div>
          <h1>Chemical Equipment Parameter Visualizer</h1>
          <p>
            Upload CSV data, review automated analytics, and download PDF
            reports. Both web and desktop clients connect to the same API.
          </p>
        </div>
        <form className="auth-form">
          <label>
            Username
            <input
              type="text"
              value={credentials.username}
              onChange={(e) =>
                setCredentials((prev) => ({ ...prev, username: e.target.value }))
              }
              placeholder="Django username"
            />
          </label>
          <label>
            Password
            <input
              type="password"
              value={credentials.password}
              onChange={(e) =>
                setCredentials((prev) => ({ ...prev, password: e.target.value }))
              }
              placeholder="Password"
            />
          </label>
        </form>
      </header>

      <main>
        <section className="panel upload-panel">
          <h2>Upload a CSV</h2>
          <p>Columns expected: Equipment Name, Type, Flowrate, Pressure, Temperature.</p>
          <form onSubmit={handleUpload}>
            <input
              type="file"
              accept=".csv"
              onChange={(e) => setSelectedFile(e.target.files[0] || null)}
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Uploading…' : 'Upload & Analyze'}
            </button>
          </form>
          {error && <p className="error-text">{error}</p>}
        </section>

        <section className="panel summary-panel">
          <h2>Latest Summary</h2>
          {latestSummary ? (
            <>
              <div className="metrics-grid">
                <div className="metric-card">
                  <span>Total Equipment</span>
                  <strong>{latestSummary.total_records}</strong>
                </div>
                <div className="metric-card">
                  <span>Avg Flowrate</span>
                  <strong>{latestSummary.avg_flowrate ?? 'N/A'}</strong>
                </div>
                <div className="metric-card">
                  <span>Avg Pressure</span>
                  <strong>{latestSummary.avg_pressure ?? 'N/A'}</strong>
                </div>
                <div className="metric-card">
                  <span>Avg Temperature</span>
                  <strong>{latestSummary.avg_temperature ?? 'N/A'}</strong>
                </div>
              </div>
              <div className="chart-wrapper">
                {Object.keys(latestSummary.type_distribution || {}).length ? (
                  <Pie data={chartData} />
                ) : (
                  <p>No equipment type data detected.</p>
                )}
              </div>
            </>
          ) : (
            <p>No uploads yet. Use the form above to get started.</p>
          )}
        </section>

        <section className="panel history-panel">
          <h2>Upload History (Last 5)</h2>
          {history.length ? (
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Filename</th>
                    <th>Uploaded</th>
                    <th>Total</th>
                    <th>Flowrate</th>
                    <th>Pressure</th>
                    <th>Temperature</th>
                    <th>Report</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((dataset) => (
                    <tr key={dataset.id}>
                      <td>{dataset.original_filename}</td>
                      <td>
                        {new Date(dataset.uploaded_at).toLocaleString()}
                      </td>
                      <td>{dataset.total_records}</td>
                      <td>{dataset.avg_flowrate ?? '—'}</td>
                      <td>{dataset.avg_pressure ?? '—'}</td>
                      <td>{dataset.avg_temperature ?? '—'}</td>
                      <td>
                        {dataset.summary_pdf ? (
                          <a
                            href={`${API_HOST}${dataset.summary_pdf}`}
                            target="_blank"
                            rel="noreferrer"
                          >
                            PDF
                          </a>
                        ) : (
                          'Pending'
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p>Upload history will appear here.</p>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
