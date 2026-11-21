import { useCallback, useEffect, useRef, useState } from 'react';

const API = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
const MAX_SIZE = 5 * 1024 * 1024;

async function request(path, options) {
  let response;
  try { response = await fetch(API + path, options); }
  catch { throw new Error('Cannot reach the backend. Start FastAPI and check VITE_API_URL.'); }
  const data = response.status === 204 ? null : await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = data && data.detail;
    throw new Error(Array.isArray(detail) ? detail.map(x => x.msg).join(', ') : detail || 'Request failed (' + response.status + ').');
  }
  return data;
}

function Skills({ title, items, tone }) {
  return <section className="result-block"><div className="block-heading"><h3>{title}</h3><span>{items.length}</span></div>
    {items.length ? <div className="chips">{items.map(item => <span className={'chip ' + (tone || '')} key={item}>{item}</span>)}</div> : <p className="muted small">No skills detected.</p>}
  </section>;
}

export default function App() {
  const [file, setFile] = useState(null);
  const [job, setJob] = useState('');
  const [role, setRole] = useState('');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [error, setError] = useState('');
  const [historyError, setHistoryError] = useState('');
  const [online, setOnline] = useState(false);
  const inputRef = useRef(null);

  const loadHistory = useCallback(async () => {
    setHistoryLoading(true);
    setHistoryError('');
    try { setHistory(await request('/api/v1/analyses?skip=0&limit=5')); }
    catch (err) { setHistoryError(err.message); }
    finally { setHistoryLoading(false); }
  }, []);

  useEffect(() => {
    let active = true;
    request('/api/v1/health').then(() => { if (active) setOnline(true); }).catch(() => { if (active) setOnline(false); });
    loadHistory();
    return () => { active = false; };
  }, [loadHistory]);

  function selectFile(candidate) {
    setError('');
    if (!candidate) return;
    const ext = candidate.name.split('.').pop().toLowerCase();
    if (!['pdf', 'docx'].includes(ext)) { setFile(null); setError('Please choose a PDF or DOCX file.'); return; }
    if (candidate.size > MAX_SIZE) { setFile(null); setError('File exceeds the 5 MB upload limit.'); return; }
    setFile(candidate);
  }

  async function submit(event) {
    event.preventDefault();
    setError('');
    setResult(null);
    if (!file) { setError('Please upload your resume first.'); return; }
    if (job.trim().length < 30) { setError('Enter a job description with at least 30 characters.'); return; }
    const body = new FormData();
    body.append('resume', file);
    body.append('job_description', job.trim());
    if (role.trim()) body.append('job_title', role.trim());
    setLoading(true);
    try {
      const data = await request('/api/v1/analyze', { method: 'POST', body });
      setResult(data);
      setOnline(true);
      await loadHistory();
    } catch (err) { setError(err.message); setOnline(false); }
    finally { setLoading(false); }
  }

  const score = result ? result.match_score : 0;

  return <div className="app-shell">
    <header className="topbar">
      <a className="brand" href="#"><span className="brand-mark">S</span><span>SWYNEX <span className="brand-light">/ RESUME LAB</span></span></a>
      <div className="topbar-right"><span className={'status-dot ' + (online ? 'online' : '')}></span><span>{online ? 'API connected' : 'API unavailable'}</span><span className="top-divider"></span><span className="project-tag">INTERNSHIP PROJECT</span></div>
    </header>

    <main className="container">
      <section className="hero">
        <div className="eyebrow"><span className="eyebrow-line"></span> CAREER TOOLKIT <span>/</span> RESUME INTELLIGENCE</div>
        <h1>Make your next move<br/><em>count.</em></h1>
        <p className="hero-copy">A clearer view of how your experience aligns with the role ahead. Upload your resume, add a job description, and get an actionable skill-match snapshot.</p>
        <div className="hero-meta"><span><b>01</b> Upload resume</span><span><b>02</b> Add role details</span><span><b>03</b> Review insights</span></div>
      </section>

      <div className="workspace">
        <section className="form-card">
          <div className="card-top"><div><span className="section-kicker">START AN ANALYSIS</span><h2>Tell us where you're headed.</h2></div><span className="step-count">01 — 03</span></div>
          <form onSubmit={submit}>
            <label className="field-label" htmlFor="resume-file">YOUR RESUME</label>
            <input ref={inputRef} id="resume-file" className="visually-hidden" type="file" accept=".pdf,.docx" onChange={e => selectFile(e.target.files && e.target.files[0])}/>
            <button type="button" className={'upload-zone ' + (file ? 'has-file' : '')} onClick={() => inputRef.current && inputRef.current.click()} onDragOver={e => e.preventDefault()} onDrop={e => { e.preventDefault(); selectFile(e.dataTransfer.files[0]); }}>
              <span className="upload-icon">{file ? '✓' : '↑'}</span><span className="upload-copy"><strong>{file ? file.name : 'Choose a file or drag it here'}</strong><small>{file ? (file.size / 1024 / 1024).toFixed(2) + ' MB · Ready to analyze' : 'PDF or DOCX · Maximum file size 5 MB'}</small></span><span className="browse-label">{file ? 'CHANGE' : 'BROWSE'}</span>
            </button>

            <label className="field-label" htmlFor="job-title">TARGET ROLE <span className="optional">OPTIONAL</span></label>
            <input id="job-title" className="text-input" value={role} onChange={e => setRole(e.target.value)} maxLength={120} placeholder="e.g. Frontend Developer Intern"/>
            <div className="label-row"><label className="field-label" htmlFor="job-description">JOB DESCRIPTION</label><span className="character-count">{job.length.toLocaleString()} / 20,000</span></div>
            <textarea id="job-description" className="text-input job-input" value={job} onChange={e => setJob(e.target.value)} minLength={30} maxLength={20000} placeholder="Paste the job description here. Include responsibilities, requirements, and skills..."/>
            {error && <div className="alert error-alert" role="alert"><span>!</span><p>{error}</p></div>}
            <button className="primary-button" type="submit" disabled={loading}>{loading ? <><span className="spinner"></span> Analyzing your resume...</> : <>Analyze my resume <span>→</span></>}</button>
            <p className="privacy-note">◇ Your resume file is processed in memory. The analysis summary is saved to the database.</p>
          </form>
        </section>

        <aside className="side-column">
          <section className="info-card"><span className="section-kicker">WHAT YOU'LL GET</span><h3>Clarity, not guesswork.</h3>
            <div className="benefit"><span>01</span><div><strong>Skill match score</strong><p>A keyword-overlap snapshot against the role.</p></div></div>
            <div className="benefit"><span>02</span><div><strong>Matched & missing skills</strong><p>See which listed skills appear in your resume.</p></div></div>
            <div className="benefit"><span>03</span><div><strong>Actionable suggestions</strong><p>Ideas to make relevant experience easier to find.</p></div></div>
          </section>
          <section className="history-card"><div className="history-heading"><div><span className="section-kicker">RECENT ACTIVITY</span><h3>Saved analyses</h3></div><button className="refresh-button" type="button" onClick={loadHistory} disabled={historyLoading} aria-label="Refresh saved analyses">↻</button></div>
            {historyLoading ? <div className="history-state"><span className="spinner dark"></span> Loading saved analyses...</div> : historyError ? <div className="history-state history-error"><p>{historyError}</p><button type="button" onClick={loadHistory}>Try again</button></div> : history.length === 0 ? <div className="history-state">No saved analyses yet. Completed reports will appear here.</div> : <ul className="history-list">{history.map(item => <li key={item.id}><span className="history-file-icon">▤</span><span className="history-file"><strong>{item.job_title || item.filename}</strong><small>{item.filename}</small></span><span className="history-score">{item.match_score}%</span></li>)}</ul>}
          </section>
        </aside>
      </div>

      {result && <section className="results-card" aria-live="polite">
        <div className="results-header"><div><span className="section-kicker">YOUR REPORT IS READY</span><h2>Here's your snapshot.</h2><p>{result.filename}{role ? ' · ' + role : ''}</p></div><span className="result-id">ID · {result.analysis_id.slice(0, 8)}</span></div>
        <div className="score-panel"><div className="score-ring" style={{background: 'conic-gradient(#4f6db6 ' + (score * 3.6) + 'deg, #e3e8f1 0)'}}><div><strong>{score}<small>%</small></strong><span>MATCH</span></div></div><div className="score-description"><strong>{score >= 75 ? 'Strong keyword overlap' : score >= 45 ? 'Some relevant skills found' : 'Room to strengthen your match'}</strong><p>This score reflects detected keyword overlap only. It is not a measure of your ability or a prediction of hiring outcomes.</p></div></div>
        <div className="skills-grid"><Skills title="Matched skills" items={result.matched_skills || []} tone="matched"/><Skills title="Skills to address" items={result.missing_skills || []} tone="missing"/><Skills title="Skills found in resume" items={result.resume_skills || []}/></div>
        <div className="suggestions"><h3>Suggestions to consider</h3><ul>{(result.suggestions || []).map((item, index) => <li key={index}><span>↗</span>{item}</li>)}</ul></div>
      </section>}

      <footer className="footer"><span>SWYNEX / RESUME LAB</span><p>Built for learning and career development. Keyword matching uses a limited skill dictionary and may miss synonyms or context.</p></footer>
    </main>
  </div>;
}
