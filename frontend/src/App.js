import React, { useState, useEffect, useRef } from 'react';
import Avatar from 'avataaars';

import AdminOpportunitiesPanel from './pages/AdminOpportunities';
const API = "";  // empty = uses proxy to localhost:8000

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  :root{
    --bg:#06070a;--surface:#0d0f14;--surface2:#13161e;
    --border:#1e2330;--border2:#252a38;
    --accent:#00e5ff;--accent2:#7c3aed;--accent3:#f59e0b;
    --success:#10b981;--danger:#ef4444;
    --text:#e8eaf0;--text2:#7c8499;--text3:#4a5068;
    --font:'Syne',sans-serif;--mono:'DM Mono',monospace;
  }
  html,body,#root{height:100%;background:var(--bg);color:var(--text);font-family:var(--font)}
  ::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:var(--surface)}::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px}
  @keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
  @keyframes spin{to{transform:rotate(360deg)}}
  .fade-up{animation:fadeUp .4s ease both}
  .fade-up-2{animation:fadeUp .4s .1s ease both}
  .fade-up-3{animation:fadeUp .4s .2s ease both}
  .app{display:flex;height:100vh;overflow:hidden}
  .sidebar{width:220px;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:24px 0;flex-shrink:0}
  .main{flex:1;overflow-y:auto;background:var(--bg)}
  .logo{padding:0 20px 24px;border-bottom:1px solid var(--border);margin-bottom:16px}
  .logo-mark{font-size:20px;font-weight:800;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
  .logo-sub{font-size:10px;font-family:var(--mono);color:var(--text3);margin-top:2px;letter-spacing:.05em}
  .nav-section{font-size:10px;font-family:var(--mono);color:var(--text3);padding:0 20px 8px;letter-spacing:.1em;text-transform:uppercase}
  .nav-item{display:flex;align-items:center;gap:10px;padding:10px 20px;font-size:13px;font-weight:600;color:var(--text2);cursor:pointer;transition:all .15s;border-left:2px solid transparent}
  .nav-item:hover{color:var(--text);background:var(--surface2)}
  .nav-item.active{color:var(--accent);background:rgba(0,229,255,.06);border-left-color:var(--accent)}
  .nav-icon{font-size:15px;width:20px;text-align:center}
  .sidebar-footer{margin-top:auto;padding:16px 20px;border-top:1px solid var(--border)}
  .avatar{width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,var(--accent2),var(--accent));display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;color:#000;flex-shrink:0}
  .user-chip{display:flex;align-items:center;gap:10px}
  .user-name{font-size:13px;font-weight:600}
  .user-role{font-size:11px;font-family:var(--mono);color:var(--text3)}
  .page{padding:32px;max-width:1100px}
  .page-title{font-size:28px;font-weight:800;margin-bottom:6px}
  .page-subtitle{font-family:var(--mono);font-size:13px;color:var(--text3)}
  .page-header{margin-bottom:28px}
  .card{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:20px}
  .card-title{font-size:11px;font-family:var(--mono);color:var(--text3);letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px}
  .ai-card{background:linear-gradient(135deg,rgba(124,58,237,.08),rgba(0,229,255,.05));border:1px solid rgba(124,58,237,.25);border-radius:14px;padding:20px}
  .ai-label{display:flex;align-items:center;gap:8px;font-size:11px;font-family:var(--mono);color:var(--accent2);letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px}
  .ai-dot{width:6px;height:6px;border-radius:50%;background:var(--accent2);animation:pulse 2s infinite}
  .grid-2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
  .grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}
  .grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
  .stat-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center}
  .stat-value{font-size:28px;font-weight:800;font-family:var(--mono);margin-bottom:4px}
  .stat-label{font-size:11px;font-family:var(--mono);color:var(--text3);text-transform:uppercase;letter-spacing:.08em}
  .stat-accent{color:var(--accent)}.stat-amber{color:var(--accent3)}.stat-purple{color:var(--accent2)}.stat-green{color:var(--success)}
  .btn{display:inline-flex;align-items:center;gap:8px;padding:10px 18px;border-radius:8px;font-family:var(--font);font-size:13px;font-weight:700;cursor:pointer;border:none;transition:all .15s}
  .btn:disabled{opacity:.5;cursor:not-allowed}
  .btn-primary{background:var(--accent);color:#000}.btn-primary:hover:not(:disabled){background:#33eaff}
  .btn-secondary{background:var(--surface2);color:var(--text);border:1px solid var(--border2)}.btn-secondary:hover:not(:disabled){border-color:var(--accent);color:var(--accent)}
  .btn-danger{background:rgba(239,68,68,.1);color:var(--danger);border:1px solid rgba(239,68,68,.2)}.btn-danger:hover{background:rgba(239,68,68,.2)}
  .btn-success{background:rgba(16,185,129,.1);color:var(--success);border:1px solid rgba(16,185,129,.2)}.btn-success:hover{background:rgba(16,185,129,.2)}
  .btn-sm{padding:6px 12px;font-size:12px}
  .form-group{margin-bottom:14px}
  .form-label{display:block;font-size:11px;font-family:var(--mono);color:var(--text3);margin-bottom:6px;letter-spacing:.05em;text-transform:uppercase}
  .form-input{width:100%;background:var(--surface2);border:1px solid var(--border2);border-radius:8px;padding:10px 14px;color:var(--text);font-family:var(--font);font-size:13px;outline:none;transition:border .15s}
  .form-input:focus{border-color:var(--accent)}
  select.form-input option{background:var(--surface2)}
  textarea.form-input{resize:vertical;min-height:80px}
  .table{width:100%;border-collapse:collapse}
  .table th{font-size:10px;font-family:var(--mono);color:var(--text3);text-transform:uppercase;letter-spacing:.08em;padding:8px 12px;text-align:left;border-bottom:1px solid var(--border)}
  .table td{padding:12px;font-size:13px;border-bottom:1px solid var(--border)}
  .table tr:last-child td{border-bottom:none}
  .badge{display:inline-flex;align-items:center;padding:3px 8px;border-radius:4px;font-size:11px;font-family:var(--mono);font-weight:500}
  .badge-blue{background:rgba(0,229,255,.1);color:var(--accent)}
  .badge-green{background:rgba(16,185,129,.1);color:var(--success)}
  .badge-amber{background:rgba(245,158,11,.1);color:var(--accent3)}
  .badge-purple{background:rgba(124,58,237,.1);color:var(--accent2)}
  .badge-red{background:rgba(239,68,68,.1);color:var(--danger)}
  .alert{padding:12px 16px;border-radius:8px;font-size:13px;margin-bottom:14px;font-family:var(--mono)}
  .alert-error{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);color:#fca5a5}
  .alert-success{background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.2);color:#6ee7b7}
  .alert-info{background:rgba(0,229,255,.07);border:1px solid rgba(0,229,255,.2);color:var(--accent)}
  .segment{display:flex;gap:4px;background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:4px;margin-bottom:20px;width:fit-content}
  .seg-btn{padding:7px 16px;border-radius:7px;font-size:12px;font-weight:600;cursor:pointer;border:none;background:transparent;color:var(--text2);transition:all .15s;font-family:var(--font)}
  .seg-btn.active{background:var(--surface2);color:var(--accent);border:1px solid var(--border2)}
  .milestone{display:flex;gap:14px;padding:12px 0;border-bottom:1px solid var(--border)}
  .milestone:last-child{border-bottom:none}
  .milestone-month{font-family:var(--mono);font-size:11px;color:var(--accent);min-width:50px;padding-top:2px}
  .milestone-goal{font-size:13px;font-weight:600;margin-bottom:3px}
  .milestone-outcome{font-size:12px;color:var(--text2);font-family:var(--mono)}
  .tag{display:inline-flex;padding:3px 10px;background:rgba(0,229,255,.07);border:1px solid rgba(0,229,255,.15);border-radius:4px;font-size:11px;font-family:var(--mono);color:var(--text2);margin:2px}
  .spinner{width:16px;height:16px;border:2px solid rgba(0,229,255,.2);border-top-color:var(--accent);border-radius:50%;animation:spin .7s linear infinite}
  .score-ring-text{font-family:var(--mono);font-weight:700;fill:var(--text)}
  .login-wrap{min-height:100vh;display:flex;align-items:center;justify-content:center;background:var(--bg);position:relative;overflow:hidden}
  .login-bg{position:absolute;inset:0;background:radial-gradient(ellipse 80% 50% at 50% 0%,rgba(124,58,237,.12) 0%,transparent 60%)}
  .drop-zone{border:2px dashed var(--border2);border-radius:12px;padding:36px 24px;text-align:center;cursor:pointer;background:var(--surface2);transition:all .2s}
  .drop-zone:hover,.drop-zone.over{border-color:var(--accent);background:rgba(0,229,255,.04)}
  .drop-zone.has-file{border-color:var(--success);background:rgba(16,185,129,.04)}
  .chat-bubble-user{max-width:70%;padding:12px 16px;border-radius:14px 14px 4px 14px;background:var(--accent);color:#000;font-size:14px;font-weight:600;align-self:flex-end}
  .chat-bubble-ai{max-width:70%;padding:12px 16px;border-radius:14px 14px 14px 4px;background:var(--surface);border:1px solid var(--border);font-size:14px;line-height:1.6;align-self:flex-start}
  .tabs{display:flex;gap:0;border-bottom:1px solid var(--border);margin-bottom:24px}
  .tab{padding:10px 20px;font-size:13px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;color:var(--text2);transition:all .15s}
  .tab.active{color:var(--accent);border-bottom-color:var(--accent)}
`;

// ── Helpers ──────────────────────────────────────────────────────────────────
const Spinner = () => <div className="spinner" />;
const Tag = ({label}) => <span className="tag">{label}</span>;

// Safely convert any AI-returned value to a renderable string
const safeStr = v => {
  if (v === null || v === undefined) return '';
  if (typeof v === 'string') return v;
  if (typeof v === 'number') return String(v);
  if (typeof v === 'object') {
    const vals = Object.values(v);
    return vals.length ? String(vals[0]) : '';
  }
  return String(v);
};

const badgeColor = b => ({Pioneer:"badge-purple",Innovator:"badge-blue",Explorer:"badge-amber",Starter:"badge-green"}[b]||"badge-blue");

async function api(path, opts={}) {
  const res = await fetch(`${API}${path}`, {
    headers: {"Content-Type":"application/json"},
    ...opts
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Request failed");
  return data;
}

async function apiForm(path, formData) {
  const res = await fetch(`${API}${path}`, {method:"POST", body:formData});
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Request failed");
  return data;
}

// ── AvatarWidget ──────────────────────────────────────────────────────────────
const AvatarWidget = ({ config, size = "100px", style = {} }) => {
  if (!config) return <div className="avatar" style={{width:size, height:size, fontSize:parseInt(size)/2.5, ...style}}>?</div>;
  
  return (
    <div style={{ position: 'relative', width: size, height: size, ...style }}>
      {/* Background Aura */}
      {config.aura && config.aura !== 'none' && (
        <div style={{
          position: 'absolute', inset: -10, borderRadius: '50%', zIndex: 0,
          background: config.aura === 'blue_glow' ? 'radial-gradient(circle, rgba(0,229,255,0.4) 0%, transparent 70%)' :
                      config.aura === 'cyan_pulse' ? 'radial-gradient(circle, rgba(0,229,255,0.6) 0%, transparent 70%)' :
                      config.aura === 'purple_crown' ? 'radial-gradient(circle, rgba(124,58,237,0.6) 0%, transparent 70%)' : 'transparent',
          animation: 'pulse 3s infinite'
        }}/>
      )}
      
      {/* The Avatar */}
      <div style={{ position: 'relative', zIndex: 1, width: '100%', height: '100%', borderRadius: '50%', overflow: 'hidden', background: 'var(--surface2)', border: '2px solid var(--border)' }}>
        <Avatar
          style={{ width: '100%', height: '100%' }}
          avatarStyle="Circle"
          topType={config.topType}
          accessoriesType={config.accessoriesType}
          hairColor={config.hairColor}
          facialHairType={config.facialHairType}
          clotheType={config.clotheType}
          clotheColor={config.clotheColor}
          eyeType={config.eyeType}
          eyebrowType={config.eyebrowType}
          mouthType={config.mouthType}
          skinColor={config.skinColor}
          graphicType={config.graphicType || 'Bat'}
        />
      </div>

      {/* Badges */}
      {config.earnedBadges && config.earnedBadges.length > 0 && (
        <div style={{ position: 'absolute', bottom: -5, right: -5, zIndex: 2, display: 'flex', gap: 2, flexWrap: 'wrap', maxWidth: '60%' }}>
          {config.earnedBadges.slice(0, 3).map((b, i) => (
            <div key={i} style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '50%', width: 20, height: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 10 }}>
              {b}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// ── ScoreRing ─────────────────────────────────────────────────────────────────
const ScoreRing = ({score=0, size=160}) => {
  const r = (size/2)-14, cx = size/2, cy = size/2;
  const circ = 2*Math.PI*r;
  const pct = Math.min(score,500)/500;
  return (
    <svg width={size} height={size} style={{flexShrink:0}}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="var(--border2)" strokeWidth="10"/>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="var(--accent)" strokeWidth="10"
        strokeDasharray={circ} strokeDashoffset={circ*(1-pct)}
        strokeLinecap="round" transform={`rotate(-90 ${cx} ${cy})`}
        style={{transition:"stroke-dashoffset .8s ease"}}/>
      <text x={cx} y={cy-8} textAnchor="middle" className="score-ring-text" fontSize={size>140?28:20}>{score}</text>
      <text x={cx} y={cy+14} textAnchor="middle" fill="var(--text3)" fontSize="11" fontFamily="var(--mono)">/500</text>
    </svg>
  );
};

// ── LOGIN ─────────────────────────────────────────────────────────────────────
const LoginPage = ({onLogin}) => {
  const [tab,setTab] = useState("student");
  const [id,setId] = useState("student_demo");
  const [loading,setLoading] = useState(false);
  const [err,setErr] = useState("");

  const login = async () => {
    if (!id.trim()) { setErr("Enter your User ID."); return; }
    if (tab==="admin") { onLogin({id:"admin_001",name:"Admin",role:"admin",email:"admin@citchennai.net"}); return; }
    setLoading(true); setErr("");
    try {
      const u = await api(`/users/${id.trim()}`);
      onLogin({...u, id:u.user_id});
    } catch { setErr("User not found. Check your User ID or register."); }
    setLoading(false);
  };

  return (
    <div className="login-wrap">
      <div className="login-bg"/>
      <div style={{background:"var(--surface)",border:"1px solid var(--border)",borderRadius:20,padding:40,width:"100%",maxWidth:420,position:"relative",zIndex:1}} className="fade-up">
        <div style={{textAlign:"center",marginBottom:32}}>
          <div style={{fontSize:32,fontWeight:800,background:"linear-gradient(135deg,var(--accent),var(--accent2))",WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent"}}>CIT RISE</div>
          <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text3)",marginTop:4}}>Research & Innovation Student Ecosystem</div>
        </div>
        <div className="tabs" style={{justifyContent:"center"}}>
          <div className={`tab ${tab==="student"?"active":""}`} onClick={()=>{setTab("student");setId("student_demo")}}>Student</div>
          <div className={`tab ${tab==="admin"?"active":""}`} onClick={()=>{setTab("admin");setId("admin_001")}}>Admin</div>
        </div>
        {err && <div className="alert alert-error">{err}</div>}
        <div className="form-group">
          <label className="form-label">{tab==="student"?"Your User ID":"Admin ID"}</label>
          <input className="form-input" value={id} onChange={e=>setId(e.target.value)}
            onKeyDown={e=>e.key==="Enter"&&login()}
            placeholder={tab==="student"?"e.g. student_demo":"admin_001"}/>
        </div>
        <button className="btn btn-primary" style={{width:"100%",justifyContent:"center",marginTop:4}} onClick={login} disabled={loading}>
          {loading?<><Spinner/> Signing in...</>:"Sign In →"}
        </button>
        {tab==="student"&&(
          <div style={{textAlign:"center",marginTop:16,fontSize:12,fontFamily:"var(--mono)",color:"var(--text3)"}}>
            No account?{" "}
            <span style={{color:"var(--accent)",cursor:"pointer"}} onClick={()=>onLogin({register:true})}>Register with PDF resume →</span>
          </div>
        )}
        <div style={{marginTop:20,padding:12,background:"var(--surface2)",borderRadius:8,fontSize:11,fontFamily:"var(--mono)",color:"var(--text3)"}}>
          Demo: use <span style={{color:"var(--accent)"}}>student_demo</span> for student or <span style={{color:"var(--accent)"}}>admin_001</span> for admin
        </div>
      </div>
    </div>
  );
};

// ── REGISTER ─────────────────────────────────────────────────────────────────
const RegisterPage = ({onComplete, onBack}) => {
  const [step,setStep] = useState(1);
  const [form,setForm] = useState({name:"",email:"",department:"",year:"2",github:""});
  const [file,setFile] = useState(null);
  const [loading,setLoading] = useState(false);
  const [err,setErr] = useState("");
  const [result,setResult] = useState(null);
  const fileRef = useRef(null);

  const register = async () => {
    if (!form.name||!form.email||!form.department){setErr("Fill all required fields.");return;}
    setLoading(true);setErr("");setStep(2);
    try {
      let uid, uname;
      if (file) {
        const fd = new FormData();
        fd.append("resume_file",file);
        fd.append("email",form.email);
        if (form.github) fd.append("github_username",form.github);
        const d = await apiForm("/users/ai-profile-from-resume",fd);
        uid=d.user_id; uname=d.profile?.name||form.name;
      } else {
        const d = await api("/users/create",{method:"POST",body:JSON.stringify({...form,year:parseInt(form.year),role:"student",skills:[],interests:[]})});
        uid=d.user_id; uname=d.user?.name||form.name;
      }
      setResult({uid,name:uname});setStep(3);
    } catch(e){setErr(e.message||"Registration failed.");setStep(1);}
    setLoading(false);
  };

  return (
    <div className="login-wrap">
      <div className="login-bg"/>
      <div style={{background:"var(--surface)",border:"1px solid var(--border)",borderRadius:20,padding:40,width:"100%",maxWidth:540,position:"relative",zIndex:1}} className="fade-up">
        <div style={{display:"flex",alignItems:"center",gap:12,marginBottom:28}}>
          <button className="btn btn-secondary btn-sm" onClick={onBack}>← Back</button>
          <div>
            <div style={{fontWeight:800,fontSize:18}}>Create CIT RISE Account</div>
            <div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)",marginTop:2}}>
              {step===1?"Fill details — optionally upload resume for AI auto-fill":step===2?"Setting up your profile...":"Welcome aboard!"}
            </div>
          </div>
        </div>

        {step===1&&(<>
          {err&&<div className="alert alert-error">{err}</div>}
          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">Full Name *</label>
              <input className="form-input" value={form.name} onChange={e=>setForm({...form,name:e.target.value})} placeholder="Shameel Ahmed"/>
            </div>
            <div className="form-group">
              <label className="form-label">Email *</label>
              <input className="form-input" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} placeholder="you@citchennai.net"/>
            </div>
            <div className="form-group">
              <label className="form-label">Department *</label>
              <select className="form-input" value={form.department} onChange={e=>setForm({...form,department:e.target.value})}>
                <option value="">Select dept</option>
                {["CSE AI","CSE","ECE","MECH","CIVIL","IT","EEE"].map(d=><option key={d}>{d}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Year</label>
              <select className="form-input" value={form.year} onChange={e=>setForm({...form,year:e.target.value})}>
                {["1","2","3","4"].map(y=><option key={y} value={y}>Year {y}</option>)}
              </select>
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">GitHub Username (optional)</label>
            <input className="form-input" value={form.github} onChange={e=>setForm({...form,github:e.target.value})} placeholder="your-github-handle"/>
          </div>
          <div className="form-group">
            <label className="form-label">Resume PDF (optional — AI auto-fills your profile)</label>
            <div className={`drop-zone ${file?"has-file":""}`} onClick={()=>fileRef.current?.click()}>
              <input ref={fileRef} type="file" accept=".pdf" style={{display:"none"}} onChange={e=>setFile(e.target.files?.[0]||null)}/>
              {file?<><div style={{fontSize:28,marginBottom:6}}>📄</div><div style={{color:"var(--success)",fontWeight:700,fontSize:13}}>{file.name}</div><div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)",marginTop:4}}>Click to change</div></>
              :<><div style={{fontSize:28,marginBottom:6}}>📁</div><div style={{color:"var(--text2)",fontSize:13,fontWeight:600}}>Drop PDF here or click to browse</div></>}
            </div>
          </div>
          <button className="btn btn-primary" style={{width:"100%",justifyContent:"center"}} onClick={register}>
            {file?"⚡ Register with AI Profile →":"Register →"}
          </button>
        </>)}

        {step===2&&(<div style={{textAlign:"center",padding:"40px 0"}}>
          <Spinner/><div style={{fontFamily:"var(--mono)",fontSize:13,color:"var(--text2)",marginTop:16}}>
            {file?"Llama AI is reading your resume...":"Creating account..."}
          </div>
        </div>)}

        {step===3&&result&&(<div style={{textAlign:"center",padding:"20px 0"}}>
          <div style={{fontSize:48,marginBottom:12}}>🎉</div>
          <div style={{fontWeight:800,fontSize:22,marginBottom:8}}>Welcome, {result.name?.split(" ")[0]}!</div>
          <div className="alert alert-info" style={{textAlign:"left"}}>
            Your User ID: <strong>{result.uid}</strong><br/>Save this — you need it to log in.
          </div>
          <button className="btn btn-primary" style={{marginTop:16}} onClick={()=>onComplete({id:result.uid,name:result.name,role:"student",email:form.email})}>
            Enter CIT RISE →
          </button>
        </div>)}
      </div>
    </div>
  );
};

// ── STUDENT DASHBOARD ─────────────────────────────────────────────────────────
const GenderPickerModal = ({ user, onComplete }) => {
  const [loading, setLoading] = useState(false);
  const finish = async (gender) => {
    setLoading(true);
    try {
      await api('/avatar/generate', { method: 'POST', body: JSON.stringify({ student_id: user.id, gender, force_regenerate: true }) });
      onComplete();
    } catch(e){ alert(e.message); setLoading(false); }
  };
  return (
    <div style={{position:"fixed",inset:0,background:"rgba(0,0,0,.8)",zIndex:500,display:"flex",alignItems:"center",justifyContent:"center"}}>
      <div className="card fade-up" style={{width:"100%",maxWidth:400,textAlign:"center"}}>
        <div style={{fontSize:48,marginBottom:10}}>🤖</div>
        <div style={{fontWeight:800,fontSize:20,marginBottom:6}}>Generate AI Avatar</div>
        <div style={{fontSize:13,color:"var(--text2)",marginBottom:24}}>Select your style for Llama to generate a personalized avatar matching your skills and domain.</div>
        <div style={{display:"flex",gap:10,justifyContent:"center"}}>
          <button className="btn btn-secondary" onClick={()=>finish("male")} disabled={loading}>{loading?<Spinner/>:"Male"}</button>
          <button className="btn btn-secondary" onClick={()=>finish("female")} disabled={loading}>{loading?<Spinner/>:"Female"}</button>
        </div>
      </div>
    </div>
  );
};

const StudentDashboard = ({user, setPage}) => {
  const [student,setStudent] = useState(null);
  const [achievements,setAchievements] = useState([]);
  const [loading,setLoading] = useState(true);
  const [showGenderModal, setShowGenderModal] = useState(false);

  useEffect(()=>{
    const load = async()=>{
      try {
        const [s,a] = await Promise.all([api(`/users/${user.id}`), api(`/achievements/${user.id}`)]);
        setStudent(s); setAchievements(a.achievements||[]);
        if (!s.avatar_config) setShowGenderModal(true);
      } catch{}
      setLoading(false);
    };
    if(user.id) load();
    else { setStudent(user); setLoading(false); }
  },[user.id]);

  if(loading) return <div style={{padding:32}}><Spinner/></div>;
  if(!student) return <div style={{padding:32,color:"var(--text3)"}}>Could not load profile.</div>;

  const badge = student.rise_score_meta?.badge || "Starter";
  const breakdown = student.rise_score_breakdown || {};

  return (
    <div className="page">
      {showGenderModal && <GenderPickerModal user={user} onComplete={()=>{setShowGenderModal(false); window.location.reload();}} />}
      <div className="page-header fade-up">
        <div className="page-title">Welcome back, {student.name?.split(" ")[0]} 👋</div>
        <div className="page-subtitle">{student.department} · Year {student.year} · CIT Chennai</div>
      </div>

      <div className="grid-2 fade-up-2" style={{marginBottom:20}}>
        <div className="card">
          <div className="card-title">Profile</div>
          <div style={{display:"flex",gap:16,marginBottom:16}}>
            <AvatarWidget config={student.avatar_config} size="80px" />
            <div style={{flex: 1}}>
              <div style={{fontWeight:700,fontSize:18}}>{student.name}</div>
              <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text3)",marginTop:2}}>{student.email}</div>
              <div style={{marginTop:8}}>
                <span className={`badge ${badgeColor(badge)}`}>🏅 {badge}</span>
                {student.avatar_config?.title && <span className="badge badge-purple" style={{marginLeft:6}}>{student.avatar_config.title}</span>}
              </div>
            </div>
          </div>
          {student.avatar_config?.avatarStory && (
            <div style={{fontStyle:"italic", fontSize:12, color:"var(--accent)", marginBottom:10, padding: 8, background:"rgba(0,229,255,0.05)", borderRadius: 6, borderLeft: "2px solid var(--accent)"}}>
              "{student.avatar_config.avatarStory}"
            </div>
          )}
          {student.ai_profile_summary&&<div style={{fontSize:13,color:"var(--text2)",lineHeight:1.6,marginBottom:12}}>{student.ai_profile_summary}</div>}
          <div style={{marginBottom:10}}>{student.skills?.map(s=><Tag key={s} label={s}/>)}</div>
          {student.innovation_potential&&<span className={`badge ${student.innovation_potential==="High"?"badge-green":"badge-amber"}`}>{student.innovation_potential} Innovation Potential</span>}
          <button className="btn btn-secondary btn-sm" style={{marginTop: 10, width: "100%", justifyContent: "center"}} onClick={async () => {
            const btn = document.getElementById('regen-btn');
            if (btn) btn.innerHTML = '<div class="spinner"></div> Regenerating...';
            try {
               await api('/users/regenerate-profile', { method: 'POST', body: JSON.stringify({student_id: user.id}) });
               window.location.reload();
            } catch (e) { alert(e.message); }
          }} id="regen-btn">🔄 Regenerate AI Summary</button>
        </div>

        <div className="card">
          <div className="card-title">CIT RISE Score</div>
          <div style={{display:"flex",gap:20,alignItems:"center"}}>
            <ScoreRing score={student.rise_score||0} size={130}/>
            <div style={{flex:1}}>
              <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text3)",marginBottom:8}}>{student.rise_score_meta?.percentile||"Not yet scored"}</div>
              {Object.entries(breakdown).map(([k,v])=>(
                <div key={k} style={{marginBottom:6}}>
                  <div style={{display:"flex",justifyContent:"space-between",fontFamily:"var(--mono)",fontSize:10,color:"var(--text3)",marginBottom:2}}>
                    <span>{k.replace(/_/g," ")}</span><span>{v}</span>
                  </div>
                  <div style={{height:4,background:"var(--border2)",borderRadius:2}}>
                    <div style={{height:4,background:"var(--accent)",borderRadius:2,width:`${Math.min(v,100)}%`,transition:"width .6s ease"}}/>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {achievements.length>0&&(
        <div className="card fade-up-3" style={{marginBottom:20}}>
          <div className="card-title">Achievements</div>
          <table className="table">
            <thead><tr><th>Title</th><th>Type</th><th>Date</th><th>Status</th></tr></thead>
            <tbody>{achievements.map(a=>(
              <tr key={a.achievement_id}>
                <td style={{fontWeight:600}}>{a.title}</td>
                <td><span className="badge badge-blue">{a.type}</span></td>
                <td style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text3)"}}>{a.date}</td>
                <td>{a.verified?<span className="badge badge-green">✓ Verified</span>:<span className="badge badge-amber">⏳ Pending</span>}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      )}

      <DailyChallengeWidget userId={user.id}/>

      {student.career_roadmap&&(
        <div className="ai-card fade-up-3" style={{marginBottom:20}}>
          <div className="ai-label"><div className="ai-dot"/>Saved Career Roadmap</div>
          <div style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}>
            <div>
              <div style={{fontWeight:700,fontSize:16}}>{safeStr(student.career_roadmap.primary_career_path)}</div>
              <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text2)",marginTop:4}}>
                {safeStr(student.career_roadmap.current_level)} · {safeStr(student.career_roadmap.time_to_job_ready)} to job-ready
              </div>
              {student.career_roadmap.motivational_note&&<div style={{fontSize:13,color:"var(--text2)",fontStyle:"italic",marginTop:8}}>"{safeStr(student.career_roadmap.motivational_note)}"</div>}
            </div>
            <button className="btn btn-secondary btn-sm" onClick={()=>setPage("roadmap")}>View Full →</button>
          </div>
        </div>
      )}

      <div style={{display:"flex",gap:10,flexWrap:"wrap"}} className="fade-up-3">
        <button className="btn btn-secondary btn-sm" onClick={()=>setPage("score")}>⚡ Update Score</button>
        <button className="btn btn-secondary btn-sm" onClick={()=>setPage("roadmap")}>🗺️ Career Roadmap</button>
        <button className="btn btn-secondary btn-sm" onClick={()=>setPage("careernav")}>🔬 CareerNav AI</button>
        <button className="btn btn-secondary btn-sm" onClick={()=>setPage("mentors")}>🤝 Find Mentors</button>
        <button className="btn btn-secondary btn-sm" onClick={()=>setPage("chat")}>💬 Ask AI</button>
      </div>
    </div>
  );
};

// ── AI PROFILE PAGE ───────────────────────────────────────────────────────────
const AIProfilePage = ({user}) => {
  const [file,setFile] = useState(null);
  const [github,setGithub] = useState("");
  const [loading,setLoading] = useState(false);
  const [result,setResult] = useState(null);
  const [err,setErr] = useState("");
  const [drag,setDrag] = useState(false);
  const fileRef = useRef(null);

  const handleFile = f => {
    if(!f) return;
    if(!f.name.toLowerCase().endsWith(".pdf")){setErr("Only PDF files supported.");return;}
    setFile(f);setErr("");
  };

  const generate = async()=>{
    if(!file){setErr("Upload your resume PDF first.");return;}
    setLoading(true);setErr("");setResult(null);
    try{
      const fd=new FormData();
      fd.append("resume_file",file);
      if(github) fd.append("github_username",github);
      const d = await apiForm("/users/ai-profile-from-resume",fd);
      setResult(d);
    }catch(e){setErr(e.message||"Failed. Make sure backend is running.");}
    setLoading(false);
  };

  return (
    <div className="page">
      <div className="page-header fade-up">
        <div className="page-title">AI Profile Generator</div>
        <div className="page-subtitle">Upload resume PDF → Llama AI builds your CIT RISE profile</div>
      </div>
      {!result?(
        <div className="grid-2 fade-up-2">
          <div className="card">
            <div className="card-title">Upload Resume</div>
            <div className={`drop-zone ${drag?"over":""} ${file?"has-file":""}`}
              onClick={()=>fileRef.current?.click()}
              onDragOver={e=>{e.preventDefault();setDrag(true)}}
              onDragLeave={()=>setDrag(false)}
              onDrop={e=>{e.preventDefault();setDrag(false);handleFile(e.dataTransfer.files[0])}}>
              <input ref={fileRef} type="file" accept=".pdf" style={{display:"none"}} onChange={e=>handleFile(e.target.files?.[0])}/>
              {file?<>
                <div style={{fontSize:36,marginBottom:8}}>📄</div>
                <div style={{fontWeight:700,color:"var(--success)",fontSize:14}}>{file.name}</div>
                <div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)",marginTop:4}}>{(file.size/1024).toFixed(1)} KB · Click to change</div>
              </>:<>
                <div style={{fontSize:36,marginBottom:8}}>📁</div>
                <div style={{fontWeight:700,color:"var(--text2)",marginBottom:4}}>Drop resume PDF here</div>
                <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text3)",marginBottom:10}}>or click to browse</div>
                <span className="badge badge-blue">PDF only</span>
              </>}
            </div>
            <div className="form-group" style={{marginTop:16}}>
              <label className="form-label">GitHub Username (optional)</label>
              <input className="form-input" value={github} onChange={e=>setGithub(e.target.value)} placeholder="your-github-handle"/>
            </div>
            {err&&<div className="alert alert-error">{err}</div>}
            <button className="btn btn-primary" style={{width:"100%",justifyContent:"center"}} onClick={generate} disabled={loading||!file}>
              {loading?<><Spinner/> Llama AI is reading your resume...</>:"⚡ Generate AI Profile"}
            </button>
            <div style={{marginTop:10,fontSize:11,fontFamily:"var(--mono)",color:"var(--text3)",textAlign:"center"}}>
              PDF must have selectable text (not a scanned image)
            </div>
          </div>
          <div className="card" style={{borderStyle:"dashed",display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center",gap:12,color:"var(--text3)"}}>
            <div style={{fontSize:48}}>🤖</div>
            <div style={{fontWeight:700,color:"var(--text2)",marginBottom:4,textAlign:"center"}}>Llama AI extracts</div>
            {["Name, department, year","Skills & tech stack","Innovation potential","Suggested career roles","AI profile summary","Initial RISE score"].map(i=>(
              <div key={i} style={{fontFamily:"var(--mono)",fontSize:12,display:"flex",gap:8}}>
                <span style={{color:"var(--accent)"}}>→</span>{i}
              </div>
            ))}
            <div style={{fontSize:11,fontFamily:"var(--mono)",color:"var(--text3)",textAlign:"center",marginTop:8}}>
              Resume text is never stored — only the profile is saved.
            </div>
          </div>
        </div>
      ):(
        <div className="fade-up">
          <div className="alert alert-success">✓ Profile generated! User ID: <strong>{result.user_id}</strong> — save this to log in.</div>
          <div className="grid-2" style={{marginBottom:16}}>
            <div className="ai-card">
              <div className="ai-label"><div className="ai-dot"/>AI Extracted Profile</div>
              <div style={{fontWeight:700,fontSize:18,marginBottom:4}}>{result.ai_extracted?.name}</div>
              <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text3)",marginBottom:10}}>{result.ai_extracted?.department} · Year {result.ai_extracted?.year}</div>
              <div style={{fontSize:13,color:"var(--text2)",lineHeight:1.6,marginBottom:12}}>{result.ai_extracted?.profile_summary}</div>
              <span className={`badge ${result.ai_extracted?.innovation_potential==="High"?"badge-green":"badge-amber"}`}>{result.ai_extracted?.innovation_potential} Potential</span>
            </div>
            <div className="card">
              <div className="card-title">Initial RISE Score</div>
              <div style={{display:"flex",alignItems:"center",gap:16}}>
                <ScoreRing score={result.initial_rise_score?.total_score||0} size={110}/>
                <div>
                  {result.initial_rise_score?.badge&&<span className={`badge ${badgeColor(result.initial_rise_score.badge)}`} style={{marginBottom:8,display:"inline-flex"}}>🏅 {result.initial_rise_score.badge}</span>}
                  <div style={{fontSize:12,color:"var(--text2)",lineHeight:1.5,marginTop:8}}>{result.initial_rise_score?.score_reasoning}</div>
                </div>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="card-title">Detected Skills</div>
            <div style={{marginBottom:12}}>{result.ai_extracted?.skills?.map(s=><Tag key={s} label={s}/>)}</div>
            <div className="card-title" style={{marginTop:12}}>Suggested Roles</div>
            <div>{result.ai_extracted?.suggested_roles?.map(r=><span key={r} className="badge badge-purple" style={{margin:3}}>{r}</span>)}</div>
          </div>
          <button className="btn btn-secondary" style={{marginTop:14}} onClick={()=>{setResult(null);setFile(null);}}>← Upload Another Resume</button>
        </div>
      )}
    </div>
  );
};

// ── RISE SCORE PAGE ───────────────────────────────────────────────────────────
const RiseScorePage = ({user}) => {
  const [student,setStudent] = useState(null);
  const [scoreData,setScoreData] = useState(null);
  const [loading,setLoading] = useState(true);
  const [recalcLoading,setRecalcLoading] = useState(false);
  const [ach,setAch] = useState({title:"",type:"hackathon",description:""});
  const [addMsg,setAddMsg] = useState("");

  useEffect(()=>{
    const load=async()=>{
      try{
        const s=await api(`/users/${user.id}`);
        setStudent(s);
        setScoreData({total_score:s.rise_score,breakdown:s.rise_score_breakdown,...(s.rise_score_meta||{})});
      }catch{}
      setLoading(false);
    };
    if(user.id) load();
  },[user.id]);

  const recalculate=async()=>{
    setRecalcLoading(true);
    try{
      const d=await api("/ai/recalculate-score",{method:"POST",body:JSON.stringify({student_id:user.id})});
      setScoreData(d.rise_score_analysis);
      const s=await api(`/users/${user.id}`); setStudent(s);
    }catch{}
    setRecalcLoading(false);
  };

  const addAchievement=async()=>{
    if(!ach.title){setAddMsg("Enter achievement title.");return;}
    try{
      await api("/achievements/add",{method:"POST",body:JSON.stringify({...ach,student_id:user.id})});
      setAddMsg("Added! Recalculating score...");
      await recalculate();
      setAch({title:"",type:"hackathon",description:""});
      setAddMsg("Achievement added & score updated.");
    }catch(e){setAddMsg(e.message||"Failed to add.");}
  };

  if(loading) return <div style={{padding:32}}><Spinner/></div>;

  const bd = scoreData?.breakdown||{};
  const dims = [{k:"achievement_quality",max:150,label:"Achievement Quality"},{k:"skill_depth",max:100,label:"Skill Depth"},
    {k:"research_impact",max:100,label:"Research Impact"},{k:"innovation_mindset",max:100,label:"Innovation Mindset"},
    {k:"leadership_potential",max:50,label:"Leadership"}];

  return (
    <div className="page">
      <div className="page-header fade-up" style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start"}}>
        <div>
          <div className="page-title">CIT RISE Score</div>
          <div className="page-subtitle">AI-calculated innovation score — not rule-based</div>
        </div>
        <button className="btn btn-primary" onClick={recalculate} disabled={recalcLoading}>
          {recalcLoading?<><Spinner/>Recalculating...</>:"⚡ Recalculate with AI"}
        </button>
      </div>

      <div className="grid-2 fade-up-2" style={{marginBottom:20}}>
        <div className="ai-card">
          <div className="ai-label"><div className="ai-dot"/>Your RISE Score</div>
          <div style={{display:"flex",gap:24,alignItems:"center"}}>
            <ScoreRing score={scoreData?.total_score||0}/>
            <div>
              {scoreData?.badge&&<span className={`badge ${badgeColor(scoreData.badge)}`} style={{marginBottom:10,display:"inline-flex",fontSize:13}}>🏅 {scoreData.badge}</span>}
              <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text2)",marginBottom:8}}>{scoreData?.percentile}</div>
              <div style={{fontSize:13,color:"var(--text2)",lineHeight:1.6}}>{scoreData?.reasoning||scoreData?.score_reasoning}</div>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-title">Score Breakdown</div>
          {dims.map(d=>(
            <div key={d.k} style={{marginBottom:10}}>
              <div style={{display:"flex",justifyContent:"space-between",fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)",marginBottom:3}}>
                <span>{d.label}</span><span>{bd[d.k]||0}/{d.max}</span>
              </div>
              <div style={{height:6,background:"var(--border2)",borderRadius:3}}>
                <div style={{height:6,background:"var(--accent)",borderRadius:3,width:`${((bd[d.k]||0)/d.max)*100}%`,transition:"width .6s ease"}}/>
              </div>
            </div>
          ))}
          {scoreData?.improvement_areas?.length>0&&(
            <>
              <div className="card-title" style={{marginTop:16}}>To Improve</div>
              {scoreData.improvement_areas.map((a,i)=>(
                <div key={i} style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text2)",marginBottom:6,display:"flex",gap:8}}>
                  <span style={{color:"var(--accent)"}}>→</span>{a}
                </div>
              ))}
            </>
          )}
        </div>
      </div>

      <div className="card fade-up-3">
        <div className="card-title">Add Achievement</div>
        <div className="grid-2">
          <div>
            <div className="form-group">
              <label className="form-label">Title *</label>
              <input className="form-input" value={ach.title} onChange={e=>setAch({...ach,title:e.target.value})} placeholder="e.g. Winner - Hackathon 2025"/>
            </div>
            <div className="form-group">
              <label className="form-label">Type</label>
              <select className="form-input" value={ach.type} onChange={e=>setAch({...ach,type:e.target.value})}>
                {["hackathon","project","research","startup","patent","certification","competition"].map(t=><option key={t}>{t}</option>)}
              </select>
            </div>
          </div>
          <div>
            <div className="form-group">
              <label className="form-label">Description</label>
              <textarea className="form-input" value={ach.description} onChange={e=>setAch({...ach,description:e.target.value})} placeholder="Briefly describe your achievement..."/>
            </div>
          </div>
        </div>
        {addMsg&&<div className="alert alert-info">{addMsg}</div>}
        <button className="btn btn-primary" onClick={addAchievement}>Add & Recalculate Score</button>
      </div>
    </div>
  );
};

// ── CAREER ROADMAP PAGE ───────────────────────────────────────────────────────
const CareerRoadmapPage = ({user}) => {
  const [roadmap,setRoadmap]   = useState(null);
  const [context,setContext]   = useState({});
  const [loading,setLoading]   = useState(false);
  const [checking,setChecking] = useState(true);

  useEffect(()=>{
    const load=async()=>{
      try{
        const s=await api(`/users/${user.id}`);
        if(s.career_roadmap) setRoadmap(s.career_roadmap);
      }catch{}
      setChecking(false);
    };
    if(user.id) load();
  },[user.id]);

  const generate=async()=>{
    setLoading(true);
    try{
      const d=await api("/ai/career-roadmap",{method:"POST",body:JSON.stringify({student_id:user.id})});
      setRoadmap(d.roadmap);
      if(d.context_used) setContext(d.context_used);
    }catch{}
    setLoading(false);
  };

  if(checking) return <div style={{padding:32}}><Spinner/></div>;

  return (
    <div className="page">
      <div className="page-header fade-up" style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start"}}>
        <div>
          <div className="page-title">Career Roadmap</div>
          <div className="page-subtitle">AI-generated personalized roadmap — powered by CareerNav × Llama</div>
        </div>
        <button className="btn btn-primary" onClick={generate} disabled={loading}>
          {loading?<><Spinner/>Generating...</>:roadmap?"🔄 Regenerate":"⚡ Generate Roadmap"}
        </button>
      </div>

      {/* Context banner — shown after generation to indicate what data was used */}
      {context.github_domain&&context.github_domain!=="—"&&(
        <div style={{display:"flex",gap:8,marginBottom:16,flexWrap:"wrap"}}>
          <span style={{fontFamily:"var(--mono)",fontSize:11,padding:"4px 10px",background:"rgba(0,229,255,.08)",border:"1px solid rgba(0,229,255,.2)",borderRadius:6,color:"var(--accent)"}}
          >GitHub: {context.github_domain}</span>
          {context.leetcode_level&&context.leetcode_level!=="—"&&(
            <span style={{fontFamily:"var(--mono)",fontSize:11,padding:"4px 10px",background:"rgba(168,85,247,.08)",border:"1px solid rgba(168,85,247,.25)",borderRadius:6,color:"var(--accent2)"}}
            >LeetCode: {context.leetcode_level}</span>
          )}
          <span style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--success)"}}>✓ Roadmap personalised using your CareerNav scans</span>
        </div>
      )}

      {!roadmap&&!loading&&(
        <div className="card fade-up" style={{textAlign:"center",padding:"60px 32px"}}>
          <div style={{fontSize:48,marginBottom:16}}>🗺️</div>
          <div style={{fontWeight:700,fontSize:18,marginBottom:8}}>No roadmap yet</div>
          <div style={{color:"var(--text3)",fontFamily:"var(--mono)",fontSize:13,marginBottom:20}}>Click "Generate Roadmap" and AI will build a plan based on your profile.</div>
          <div style={{display:"inline-flex",gap:8,alignItems:"center",padding:"10px 16px",background:"rgba(0,229,255,.06)",border:"1px solid rgba(0,229,255,.15)",borderRadius:8}}>
            <span style={{fontSize:14}}>💡</span>
            <span style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text2)"}}>For a smarter roadmap: run <strong>CareerNav → GitHub Analysis</strong> and <strong>LeetCode Analysis</strong> first</span>
          </div>
        </div>
      )}

      {roadmap&&(
        <div className="fade-up">
          <div className="grid-3" style={{marginBottom:20}}>
            <div className="stat-card"><div className="stat-value stat-accent" style={{fontSize:18}}>{safeStr(roadmap.primary_career_path)}</div><div className="stat-label">Career Path</div></div>
            <div className="stat-card"><div className="stat-value stat-purple" style={{fontSize:22}}>{safeStr(roadmap.current_level)}</div><div className="stat-label">Current Level</div></div>
            <div className="stat-card"><div className="stat-value stat-amber" style={{fontSize:22}}>{safeStr(roadmap.time_to_job_ready)}</div><div className="stat-label">To Job-Ready</div></div>
          </div>

          {roadmap.motivational_note&&(
            <div className="ai-card" style={{marginBottom:20}}>
              <div className="ai-label"><div className="ai-dot"/>AI Note</div>
              <div style={{fontSize:15,fontStyle:"italic",color:"var(--text2)"}}>"{safeStr(roadmap.motivational_note)}"</div>
            </div>
          )}

          <div className="grid-2" style={{marginBottom:20}}>
            <div className="card">
              <div className="card-title">Immediate Actions</div>
              {roadmap.immediate_actions?.map((a,i)=>(
                <div key={i} style={{marginBottom:14,paddingBottom:14,borderBottom:"1px solid var(--border)"}}>
                  <div style={{fontWeight:600,marginBottom:4}}>{safeStr(a.action)}</div>
                  <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text3)"}}>{safeStr(a.timeline)} · {safeStr(a.why)}</div>
                </div>
              ))}
            </div>
            <div className="card">
              <div className="card-title">Skill Gaps</div>
              {roadmap.skill_gaps?.map((g,i)=>(
                <div key={i} style={{marginBottom:12}}>
                  <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:4}}>
                    <span style={{fontWeight:600,fontSize:13}}>{safeStr(g.skill)}</span>
                    <span className={`badge ${safeStr(g.priority)==="High"?"badge-red":"badge-amber"}`}>{safeStr(g.priority)}</span>
                  </div>
                  <div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)"}}>{safeStr(g.resource)}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="card" style={{marginBottom:20}}>
            <div className="card-title">Month-by-Month Milestones</div>
            {roadmap.milestones?.map((m,i)=>(
              <div key={i} className="milestone">
                <div className="milestone-month">Mo. {m.month}</div>
                <div><div className="milestone-goal">{safeStr(m.goal)}</div><div className="milestone-outcome">{safeStr(m.outcome)}</div></div>
              </div>
            ))}
          </div>

          <div className="grid-2">
            <div className="card">
              <div className="card-title">Recommended Projects</div>
              {roadmap.recommended_projects?.map((p,i)=>(
                <div key={i} style={{fontFamily:"var(--mono)",fontSize:13,color:"var(--text2)",marginBottom:8,display:"flex",gap:8}}>
                  <span style={{color:"var(--accent)"}}>▸</span>{safeStr(p)}
                </div>
              ))}
            </div>
            <div className="card">
              <div className="card-title">Salary Outlook</div>
              <div style={{display:"flex",gap:20}}>
                <div className="stat-card" style={{flex:1}}>
                  <div className="stat-value stat-green" style={{fontSize:20}}>{safeStr(roadmap.salary_outlook?.fresher)}</div>
                  <div className="stat-label">Fresher</div>
                </div>
                <div className="stat-card" style={{flex:1}}>
                  <div className="stat-value stat-accent" style={{fontSize:20}}>{safeStr(roadmap.salary_outlook?.["3_years"])}</div>
                  <div className="stat-label">3 Years</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// ── CAREERNAV PAGE ────────────────────────────────────────────────────────────
const CareerNavPage = ({user}) => {
  const [tab,setTab] = useState("github");
  const [ghUser,setGhUser] = useState(""); const [ghResult,setGhResult] = useState(null); const [ghLoad,setGhLoad] = useState(false); const [ghErr,setGhErr] = useState("");
  const [lcUser,setLcUser] = useState(""); const [lcResult,setLcResult] = useState(null); const [lcLoad,setLcLoad] = useState(false); const [lcErr,setLcErr] = useState("");

  const analyzeGH=async()=>{
    if(!ghUser.trim())return;
    setGhLoad(true);setGhErr("");setGhResult(null);
    try{const d=await api("/careernav/github",{method:"POST",body:JSON.stringify({username:ghUser.trim(),student_id:user.id})});setGhResult(d);}
    catch(e){setGhErr(e.message||"Not found or GitHub unavailable.");}
    setGhLoad(false);
  };
  const analyzeLC=async()=>{
    if(!lcUser.trim())return;
    setLcLoad(true);setLcErr("");setLcResult(null);
    try{const d=await api("/careernav/leetcode",{method:"POST",body:JSON.stringify({username:lcUser.trim(),student_id:user.id})});setLcResult(d);}
    catch(e){setLcErr(e.message||"Not found or LeetCode unavailable.");}
    setLcLoad(false);
  };

  return (
    <div className="page">
      <div className="page-header fade-up" style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}>
        <div><div className="page-title">CareerNav AI</div><div className="page-subtitle">Live GitHub + LeetCode analysis — real data, AI insights</div></div>
        <span className="badge badge-purple">CareerNav × CIT RISE</span>
      </div>
      <div className="segment fade-up-2">
        <button className={`seg-btn ${tab==="github"?"active":""}`} onClick={()=>setTab("github")}>GitHub Analysis</button>
        <button className={`seg-btn ${tab==="leetcode"?"active":""}`} onClick={()=>setTab("leetcode")}>LeetCode Analysis</button>
      </div>

      {tab==="github"&&(
        <div className="fade-up">
          <div className="card" style={{marginBottom:16}}>
            <div style={{display:"flex",gap:10}}>
              <input className="form-input" style={{flex:1}} placeholder="Enter GitHub username e.g. torvalds"
                value={ghUser} onChange={e=>setGhUser(e.target.value)} onKeyDown={e=>e.key==="Enter"&&analyzeGH()}/>
              <button className="btn btn-primary" onClick={analyzeGH} disabled={ghLoad||!ghUser.trim()}>
                {ghLoad?<><Spinner/>Analyzing...</>:"Analyze →"}
              </button>
            </div>
            {ghErr&&<div className="alert alert-error" style={{marginTop:10}}>{ghErr}</div>}
          </div>
          {ghResult&&(
            <div className="fade-up">
              <div className="grid-3" style={{marginBottom:16}}>
                {[{l:"Repos",v:ghResult.raw?.public_repos,c:"stat-accent"},{l:"Stars",v:ghResult.raw?.total_stars,c:"stat-amber"},{l:"Followers",v:ghResult.raw?.followers,c:"stat-purple"}].map(s=>(
                  <div className="stat-card" key={s.l}><div className={`stat-value ${s.c}`}>{s.v??0}</div><div className="stat-label">{s.l}</div></div>
                ))}
              </div>

              {/* ── Overview + Skills ── */}
              <div className="grid-2" style={{marginBottom:16}}>
                <div className="ai-card">
                  <div className="ai-label"><div className="ai-dot"/>Llama Analysis</div>
                  <div style={{fontWeight:700,fontSize:16,marginBottom:6}}>{ghResult.ai_analysis?.developer_level} Developer</div>
                  <div style={{fontSize:13,color:"var(--text2)",lineHeight:1.6,marginBottom:10}}>{ghResult.ai_analysis?.github_summary}</div>
                  <div style={{display:"flex",gap:6,flexWrap:"wrap",marginBottom:10}}>
                    <span className="badge badge-blue">{ghResult.ai_analysis?.primary_domain}</span>
                    <span className="badge badge-green">{ghResult.ai_analysis?.career_readiness}</span>
                  </div>
                  {ghResult.profile_enriched&&<div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--success)"}}>✓ Skills merged into RISE profile · New score: {ghResult.new_rise_score}</div>}
                </div>
                <div className="card">
                  <div className="card-title">Detected Skills</div>
                  <div>{ghResult.ai_analysis?.detected_skills?.map(s=><Tag key={s} label={s}/>)}</div>
                </div>
              </div>

              {/* ── Strengths & Weaknesses ── */}
              <div className="grid-2" style={{marginBottom:16}}>
                <div className="card">
                  <div className="card-title" style={{color:"var(--success)"}}>✓ Portfolio Strengths</div>
                  {ghResult.ai_analysis?.portfolio_strengths?.length>0
                    ? ghResult.ai_analysis.portfolio_strengths.map((s,i)=>(
                        <div key={i} style={{display:"flex",gap:10,marginBottom:8,alignItems:"flex-start"}}>
                          <span style={{color:"var(--success)",fontSize:16,lineHeight:1}}>✓</span>
                          <span style={{fontSize:13,color:"var(--text2)",lineHeight:1.5}}>{s}</span>
                        </div>
                      ))
                    : <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text3)"}}>No strengths detected yet.</div>
                  }
                </div>
                <div className="card">
                  <div className="card-title" style={{color:"var(--danger)"}}>✗ Portfolio Weaknesses</div>
                  {ghResult.ai_analysis?.portfolio_weaknesses?.length>0
                    ? ghResult.ai_analysis.portfolio_weaknesses.map((w,i)=>(
                        <div key={i} style={{display:"flex",gap:10,marginBottom:8,alignItems:"flex-start"}}>
                          <span style={{color:"var(--danger)",fontSize:16,lineHeight:1}}>✗</span>
                          <span style={{fontSize:13,color:"var(--text2)",lineHeight:1.5}}>{w}</span>
                        </div>
                      ))
                    : <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text3)"}}>No weaknesses detected.</div>
                  }
                </div>
              </div>

              {/* ── Improvement Recommendations ── */}
              {ghResult.ai_analysis?.improvement_recommendations?.length>0&&(
                <div className="card" style={{marginBottom:16}}>
                  <div className="card-title">🚀 Improvement Recommendations</div>
                  {ghResult.ai_analysis.improvement_recommendations.map((r,i)=>(
                    <div key={i} style={{marginBottom:16,paddingBottom:16,borderBottom:i<ghResult.ai_analysis.improvement_recommendations.length-1?"1px solid var(--border)":"none"}}>
                      <div style={{fontWeight:700,fontSize:14,marginBottom:4,color:"var(--accent)"}}>{r.action}</div>
                      <div style={{fontSize:13,color:"var(--text2)",marginBottom:6,lineHeight:1.5}}>{r.reason}</div>
                      {r.example_project&&(
                        <div style={{display:"flex",gap:8,alignItems:"center"}}>
                          <span style={{fontFamily:"var(--mono)",fontSize:10,color:"var(--text3)",textTransform:"uppercase",letterSpacing:".05em"}}>Try:</span>
                          <span style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--accent2)",fontStyle:"italic"}}>{r.example_project}</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {/* ── Top Repos ── */}
              {ghResult.raw?.top_repos?.length>0&&(
                <div className="card">
                  <div className="card-title">Top Repositories</div>
                  <table className="table">
                    <thead><tr><th>Repo</th><th>Language</th><th>Stars</th></tr></thead>
                    <tbody>{ghResult.raw.top_repos.slice(0,6).map(r=>(
                      <tr key={r.name}>
                        <td><div style={{fontWeight:600}}>{r.name}</div>{r.description&&<div style={{fontSize:11,color:"var(--text3)",fontFamily:"var(--mono)",marginTop:2}}>{r.description.slice(0,70)}{r.description.length>70?"…":""}</div>}</td>
                        <td>{r.language?<span className="badge badge-blue">{r.language}</span>:"—"}</td>
                        <td style={{fontFamily:"var(--mono)",color:"var(--accent3)"}}>⭐ {r.stars}</td>
                      </tr>
                    ))}</tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {tab==="leetcode"&&(
        <div className="fade-up">
          <div className="card" style={{marginBottom:16}}>
            <div style={{display:"flex",gap:10}}>
              <input className="form-input" style={{flex:1}} placeholder="Enter LeetCode username"
                value={lcUser} onChange={e=>setLcUser(e.target.value)} onKeyDown={e=>e.key==="Enter"&&analyzeLC()}/>
              <button className="btn btn-primary" onClick={analyzeLC} disabled={lcLoad||!lcUser.trim()}>
                {lcLoad?<><Spinner/>Analyzing...</>:"Analyze →"}
              </button>
            </div>
            {lcErr&&<div className="alert alert-error" style={{marginTop:10}}>{lcErr}</div>}
          </div>
          {lcResult&&(
            <div className="fade-up">
              {/* ── Solved counts ── */}
              <div className="grid-4" style={{marginBottom:16}}>
                {[{l:"Total",v:lcResult.raw?.solved?.total,c:"stat-accent"},{l:"Easy",v:lcResult.raw?.solved?.easy,c:"stat-green"},
                  {l:"Medium",v:lcResult.raw?.solved?.medium,c:"stat-amber"},{l:"Hard",v:lcResult.raw?.solved?.hard,c:"stat-purple"}].map(s=>(
                  <div className="stat-card" key={s.l}><div className={`stat-value ${s.c}`}>{s.v??0}</div><div className="stat-label">{s.l}</div></div>
                ))}
              </div>

              {/* ── Assessment + Strong/Weak ── */}
              <div className="grid-2" style={{marginBottom:16}}>
                <div className="ai-card">
                  <div className="ai-label"><div className="ai-dot"/>Llama Assessment</div>
                  <div style={{fontWeight:700,fontSize:18,marginBottom:6}}>{lcResult.ai_analysis?.dsa_level}</div>
                  {lcResult.ai_analysis?.level_explanation&&(
                    <div style={{fontSize:13,color:"var(--text2)",lineHeight:1.6,marginBottom:10,padding:"8px 12px",background:"rgba(0,229,255,.05)",borderRadius:8,borderLeft:"3px solid var(--accent)"}}>
                      {lcResult.ai_analysis.level_explanation}
                    </div>
                  )}
                  <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--accent3)",marginBottom:10}}>
                    {lcResult.ai_analysis?.interview_readiness}
                  </div>
                  <div style={{fontSize:13,color:"var(--text2)",lineHeight:1.6,marginBottom:10}}>{lcResult.ai_analysis?.lc_summary}</div>
                  <div style={{marginBottom:10}}>{lcResult.ai_analysis?.company_targets?.map(c=><span key={c} className="badge badge-purple" style={{margin:2}}>{c}</span>)}</div>
                  {lcResult.ai_analysis?.milestone_goals?.length>0&&(
                    <>
                      <div style={{fontFamily:"var(--mono)",fontSize:10,color:"var(--text3)",textTransform:"uppercase",letterSpacing:".08em",marginBottom:6}}>Milestone Goals</div>
                      {lcResult.ai_analysis.milestone_goals.map((g,i)=>(
                        <div key={i} style={{display:"flex",gap:8,marginBottom:4,fontSize:12,color:"var(--accent)",fontFamily:"var(--mono)"}}>
                          <span>→</span>{g}
                        </div>
                      ))}
                    </>
                  )}
                </div>
                <div className="card">
                  <div className="card-title" style={{color:"var(--success)"}}>✓ Strong Areas</div>
                  {lcResult.ai_analysis?.strong_areas?.map((a,i)=>(
                    <div key={i} style={{display:"flex",gap:8,marginBottom:6,fontSize:13,color:"var(--text2)"}}>
                      <span style={{color:"var(--success)"}}>✓</span>{a}
                    </div>
                  ))}
                  <div className="card-title" style={{marginTop:14,color:"var(--danger)"}}>✗ Weak Areas</div>
                  {lcResult.ai_analysis?.weak_areas?.map((a,i)=>(
                    <div key={i} style={{display:"flex",gap:8,marginBottom:6,fontSize:13,color:"var(--text2)"}}>
                      <span style={{color:"var(--danger)"}}>✗</span>{a}
                    </div>
                  ))}
                </div>
              </div>

              {/* ── Concept Gaps ── */}
              {lcResult.ai_analysis?.concept_gaps?.length>0&&(
                <div className="card" style={{marginBottom:16,borderColor:"rgba(245,158,11,.25)",background:"rgba(245,158,11,.03)"}}>
                  <div className="card-title" style={{color:"var(--accent3)"}}>🧠 Concept Gaps to Bridge</div>
                  <div style={{display:"flex",flexWrap:"wrap",gap:8}}>
                    {lcResult.ai_analysis.concept_gaps.map((g,i)=>(
                      <span key={i} style={{
                        padding:"5px 12px",
                        background:"rgba(245,158,11,.1)",
                        border:"1px solid rgba(245,158,11,.25)",
                        borderRadius:6,
                        fontFamily:"var(--mono)",
                        fontSize:12,
                        color:"var(--accent3)"
                      }}>{g}</span>
                    ))}
                  </div>
                </div>
              )}

              {/* ── Improvement Plan ── */}
              {lcResult.ai_analysis?.improvement_plan?.length>0&&(
                <div className="card" style={{marginBottom:16}}>
                  <div className="card-title">📚 Improvement Plan</div>
                  {lcResult.ai_analysis.improvement_plan.map((p,i)=>(
                    <div key={i} style={{marginBottom:14,paddingBottom:14,borderBottom:i<lcResult.ai_analysis.improvement_plan.length-1?"1px solid var(--border)":"none"}}>
                      <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:4}}>
                        <span style={{fontWeight:700,fontSize:14}}>{p.focus_topic}</span>
                        <span className="badge badge-amber">{p.target_problems} problems</span>
                      </div>
                      <div style={{fontSize:13,color:"var(--text2)",fontFamily:"var(--mono)"}}>{p.reason}</div>
                    </div>
                  ))}
                </div>
              )}

              {/* ── Weekly Practice Plan ── */}
              {lcResult.ai_analysis?.weekly_practice_plan?.length>0&&(
                <div className="card">
                  <div className="card-title">📅 Weekly Practice Schedule</div>
                  {lcResult.ai_analysis.weekly_practice_plan.map((w,i)=>(
                    <div key={i} className="milestone">
                      <div className="milestone-month">Wk {w.week}</div>
                      <div>
                        <div className="milestone-goal">{w.focus}</div>
                        <div className="milestone-outcome">Target: {w.target}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// ── MENTORS PAGE ──────────────────────────────────────────────────────────────
const MentorsPage = ({user}) => {
  const [mentors,setMentors] = useState([]);
  const [recs,setRecs] = useState([]);
  const [tab,setTab] = useState("all");
  const [loading,setLoading] = useState(true);
  const [showAdd,setShowAdd] = useState(false);
  const [form,setForm] = useState({name:"",company:"",domain:"",skills:"",bio:"",linkedin:""});
  const [chatMentor,setChatMentor] = useState(null);
  const [messages,setMessages] = useState([]);
  const [msgText,setMsgText] = useState("");
  const [msgLoading,setMsgLoading] = useState(false);
  const chatEndRef = useRef(null);

  const openChat = async (mentor) => {
    setChatMentor(mentor);
    try {
      const d = await api(`/chat/conversation/${user.id}/${mentor.mentor_id}`);
      setMessages(d.messages||[]);
    } catch { setMessages([]); }
  };

  useEffect(()=>{ chatEndRef.current?.scrollIntoView({behavior:"smooth"}); },[messages]);

  const sendMessage = async () => {
    const text = msgText.trim();
    if(!text||!chatMentor) return;
    setMsgText(""); setMsgLoading(true);
    try {
      await api("/chat/message",{method:"POST",body:JSON.stringify({student_id:user.id,mentor_id:chatMentor.mentor_id,text,sender:"student"})});
      const d = await api(`/chat/conversation/${user.id}/${chatMentor.mentor_id}`);
      setMessages(d.messages||[]);
    } catch {}
    setMsgLoading(false);
  };

  useEffect(()=>{
    const load=async()=>{
      try{
        const [m,r]=await Promise.all([api("/mentors/"),user.id?api(`/mentors/recommend/${user.id}`):Promise.resolve({recommended_mentors:[]})]);
        setMentors(m.mentors||[]); setRecs(r.recommended_mentors||[]);
      }catch{}
      setLoading(false);
    };
    load();
  },[user.id]);

  const addMentor=async()=>{
    try{
      await api("/mentors/add",{method:"POST",body:JSON.stringify({...form,skills:form.skills.split(",").map(s=>s.trim()).filter(Boolean)})});
      const m=await api("/mentors/"); setMentors(m.mentors||[]);
      setShowAdd(false);setForm({name:"",company:"",domain:"",skills:"",bio:"",linkedin:""});
    }catch{}
  };

  const list = tab==="recommended"?recs:mentors;

  return (
    <div className="page">
      <div className="page-header fade-up" style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start"}}>
        <div><div className="page-title">Mentors</div><div className="page-subtitle">Alumni & industry mentors available for guidance</div></div>
        {user.role==="admin"&&<button className="btn btn-primary" onClick={()=>setShowAdd(!showAdd)}>+ Add Mentor</button>}
      </div>
      {showAdd&&(
        <div className="card" style={{marginBottom:20}}>
          <div className="card-title">Add New Mentor</div>
          <div className="grid-2">
            <div>
              <div className="form-group"><label className="form-label">Name</label><input className="form-input" value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/></div>
              <div className="form-group"><label className="form-label">Company</label><input className="form-input" value={form.company} onChange={e=>setForm({...form,company:e.target.value})}/></div>
              <div className="form-group"><label className="form-label">Domain</label><input className="form-input" placeholder="e.g. Machine Learning" value={form.domain} onChange={e=>setForm({...form,domain:e.target.value})}/></div>
            </div>
            <div>
              <div className="form-group"><label className="form-label">Skills (comma separated)</label><input className="form-input" placeholder="Python, ML, Docker" value={form.skills} onChange={e=>setForm({...form,skills:e.target.value})}/></div>
              <div className="form-group"><label className="form-label">Bio</label><textarea className="form-input" value={form.bio} onChange={e=>setForm({...form,bio:e.target.value})}/></div>
              <div className="form-group"><label className="form-label">LinkedIn</label><input className="form-input" value={form.linkedin} onChange={e=>setForm({...form,linkedin:e.target.value})}/></div>
            </div>
          </div>
          <button className="btn btn-primary" onClick={addMentor}>Add Mentor</button>
          <button className="btn btn-secondary" style={{marginLeft:10}} onClick={()=>setShowAdd(false)}>Cancel</button>
        </div>
      )}
      <div className="segment fade-up-2">
        <button className={`seg-btn ${tab==="all"?"active":""}`} onClick={()=>setTab("all")}>All Mentors ({mentors.length})</button>
        <button className={`seg-btn ${tab==="recommended"?"active":""}`} onClick={()=>setTab("recommended")}>🎯 Recommended ({recs.length})</button>
      </div>
      {loading?<Spinner/>:(
        <div className="grid-2 fade-up-3">
          {list.map(m=>(
            <div className="card" key={m.mentor_id}>
              <div style={{display:"flex",gap:12,marginBottom:10}}>
                <div className="avatar" style={{width:42,height:42,borderRadius:10,fontSize:17,flexShrink:0}}>{m.name?.[0]}</div>
                <div style={{flex:1}}>
                  <div style={{fontWeight:700}}>{m.name}</div>
                  <div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)"}}>{m.company}</div>
                </div>
                <span className="badge badge-blue">{m.domain}</span>
              </div>
              {m.bio&&<div style={{fontSize:13,color:"var(--text2)",lineHeight:1.5,marginBottom:10}}>{m.bio}</div>}
              <div style={{marginBottom:8}}>{m.skills?.map(s=><Tag key={s} label={s}/>)}</div>
              {m.match_score>0&&<div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--success)",marginBottom:8}}>✓ {m.match_score}% skill match</div>}
              <div style={{display:"flex",gap:8,alignItems:"center",marginTop:8, flexWrap:"wrap"}}>
                {m.linkedin&&<a href={`https://${m.linkedin}`} target="_blank" rel="noreferrer" style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--accent)",textDecoration:"none"}}>LinkedIn →</a>}
                {user.role==="student"&&<button className="btn btn-secondary btn-sm" style={{marginLeft:"auto"}} onClick={()=>openChat(m)}>💬 Message</button>}
                {user.role==="admin"&&<button className="btn btn-secondary btn-sm" style={{marginLeft:"auto"}} onClick={async ()=>{
                    const title = prompt("Edit Mentor bio:", m.bio || "");
                    if(title !== null) {
                      try { await api(`/mentors/${m.mentor_id}`, {method:"PUT", body:JSON.stringify({bio: title})}); const [ma,r]=await Promise.all([api("/mentors/"),api(`/mentors/recommend/${user.id||"admin"}`)]); setMentors(ma.mentors||[]); setRecs(r.recommended_mentors||[]); } catch(e){alert(e.message)}
                    }
                }}>Edit</button>}
                {user.role==="admin"&&<button className="btn btn-danger btn-sm" onClick={async ()=>{
                    if(window.confirm("Delete this mentor?")) {
                      try { await api(`/mentors/${m.mentor_id}`, {method:"DELETE"}); const [ma,r]=await Promise.all([api("/mentors/"),api(`/mentors/recommend/${user.id||"admin"}`)]); setMentors(ma.mentors||[]); setRecs(r.recommended_mentors||[]); } catch(e){alert(e.message)}
                    }
                }}>Delete</button>}
              </div>
            </div>
          ))}
          {list.length===0&&<div style={{gridColumn:"1/-1",textAlign:"center",padding:48,color:"var(--text3)",fontFamily:"var(--mono)"}}>{tab==="recommended"?"Complete your profile first.":"No mentors yet."}</div>}
        </div>
      )}

      {chatMentor&&(
        <div style={{position:"fixed",inset:0,background:"rgba(0,0,0,.7)",zIndex:300,display:"flex",alignItems:"center",justifyContent:"center"}}>
          <div style={{background:"var(--surface)",border:"1px solid var(--border)",borderRadius:16,width:"100%",maxWidth:520,height:520,display:"flex",flexDirection:"column",overflow:"hidden"}}>
            <div style={{padding:"16px 20px",borderBottom:"1px solid var(--border)",display:"flex",alignItems:"center",gap:12}}>
              <div className="avatar" style={{flexShrink:0}}>{chatMentor.name?.[0]}</div>
              <div style={{flex:1}}>
                <div style={{fontWeight:700}}>{chatMentor.name}</div>
                <div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)"}}>{chatMentor.company} · {chatMentor.domain}</div>
              </div>
              <button className="btn btn-secondary btn-sm" onClick={()=>setChatMentor(null)}>✕ Close</button>
            </div>
            <div style={{flex:1,overflowY:"auto",padding:16,display:"flex",flexDirection:"column",gap:10}}>
              {messages.length===0&&<div style={{textAlign:"center",color:"var(--text3)",fontFamily:"var(--mono)",fontSize:12,marginTop:40}}>No messages yet. Say hello!</div>}
              {messages.map((m,i)=>(
                <div key={i} style={{display:"flex",justifyContent:m.sender==="student"?"flex-end":"flex-start"}}>
                  <div style={{maxWidth:"75%",padding:"10px 14px",borderRadius:m.sender==="student"?"14px 14px 4px 14px":"14px 14px 14px 4px",background:m.sender==="student"?"var(--accent)":"var(--surface2)",color:m.sender==="student"?"#000":"var(--text)",fontSize:13}}>
                    {m.text}
                    <div style={{fontSize:10,fontFamily:"var(--mono)",opacity:.6,marginTop:4,textAlign:"right"}}>{m.timestamp?.slice(11,16)}</div>
                  </div>
                </div>
              ))}
              <div ref={chatEndRef}/>
            </div>
            <div style={{padding:"12px 16px",borderTop:"1px solid var(--border)",display:"flex",gap:8}}>
              <input className="form-input" style={{flex:1}} placeholder="Type a message..." value={msgText} onChange={e=>setMsgText(e.target.value)} onKeyDown={e=>e.key==="Enter"&&sendMessage()}/>
              <button className="btn btn-primary" onClick={sendMessage} disabled={msgLoading||!msgText.trim()}>{msgLoading?<Spinner/>:"Send →"}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// ── OPPORTUNITIES PAGE ────────────────────────────────────────────────────────
const OpportunitiesPage = ({user}) => {
  const [opps,setOpps] = useState([]);
  const [filter,setFilter] = useState("all");
  const [loading,setLoading] = useState(true);
  const [showAdd,setShowAdd] = useState(false);
  const [form,setForm] = useState({title:"",description:"",domain:"",deadline:"",type:"internship"});

  useEffect(()=>{
    const load=async()=>{try{const d=await api("/opportunities/");setOpps(d.opportunities||[]);}catch{}setLoading(false);};
    load();
  },[]);

  const createOpp=async()=>{
    try{
      await api("/opportunities/create",{method:"POST",body:JSON.stringify(form)});
      const d=await api("/opportunities/");setOpps(d.opportunities||[]);
      setShowAdd(false);setForm({title:"",description:"",domain:"",deadline:"",type:"internship"});
    }catch{}
  };
  const deleteOpp=async(id)=>{
    try{await api(`/opportunities/${id}`,{method:"DELETE"});const d=await api("/opportunities/");setOpps(d.opportunities||[]);}catch{}
  };

  const typeColor = t=>({internship:"badge-blue",competition:"badge-purple",research:"badge-green",job:"badge-amber",grant:"badge-amber"}[t]||"badge-blue");
  const filtered = filter==="all"?opps:opps.filter(o=>o.type===filter);

  return (
    <div className="page">
      <div className="page-header fade-up" style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start"}}>
        <div><div className="page-title">Opportunities</div><div className="page-subtitle">Internships, competitions, research openings</div></div>
        {user.role==="admin"&&<button className="btn btn-primary" onClick={()=>setShowAdd(!showAdd)}>+ Post Opportunity</button>}
      </div>
      {showAdd&&(
        <div className="card" style={{marginBottom:20}}>
          <div className="card-title">Post New Opportunity</div>
          <div className="grid-2">
            <div>
              <div className="form-group"><label className="form-label">Title</label><input className="form-input" value={form.title} onChange={e=>setForm({...form,title:e.target.value})}/></div>
              <div className="form-group"><label className="form-label">Domain</label><input className="form-input" placeholder="e.g. AI/ML, Startup" value={form.domain} onChange={e=>setForm({...form,domain:e.target.value})}/></div>
              <div className="form-group">
                <label className="form-label">Type</label>
                <select className="form-input" value={form.type} onChange={e=>setForm({...form,type:e.target.value})}>
                  {["internship","competition","research","job","grant"].map(t=><option key={t}>{t}</option>)}
                </select>
              </div>
            </div>
            <div>
              <div className="form-group"><label className="form-label">Description</label><textarea className="form-input" value={form.description} onChange={e=>setForm({...form,description:e.target.value})}/></div>
              <div className="form-group"><label className="form-label">Deadline</label><input className="form-input" type="date" value={form.deadline} onChange={e=>setForm({...form,deadline:e.target.value})}/></div>
            </div>
          </div>
          <button className="btn btn-primary" onClick={createOpp}>Post</button>
          <button className="btn btn-secondary" style={{marginLeft:10}} onClick={()=>setShowAdd(false)}>Cancel</button>
        </div>
      )}
      <div className="segment fade-up-2">
        {["all","internship","competition","research","job"].map(t=>(
          <button key={t} className={`seg-btn ${filter===t?"active":""}`} onClick={()=>setFilter(t)}>{t[0].toUpperCase()+t.slice(1)}</button>
        ))}
      </div>
      {loading?<Spinner/>:(
        <div className="grid-2 fade-up-3">
          {filtered.map(o=>(
            <div className="card" key={o.opportunity_id}>
              <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:8}}>
                <div>
                  <div style={{fontWeight:700,fontSize:15,marginBottom:4}}>{o.title}</div>
                  <span className={`badge ${typeColor(o.type)}`}>{o.type}</span>
                  {o.domain&&<span className="badge badge-blue" style={{marginLeft:4}}>{o.domain}</span>}
                </div>
                {user.role==="admin"&&<button className="btn btn-danger btn-sm" onClick={()=>deleteOpp(o.opportunity_id)}>Delete</button>}
              </div>
              <div style={{fontSize:13,color:"var(--text2)",lineHeight:1.5,marginBottom:10}}>{o.description}</div>
              <div style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}>
                {o.deadline ? <div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)"}}>Deadline: {o.deadline}</div> : <div/>}
                {o.source_url && <a href={o.source_url} target="_blank" rel="noreferrer" className="btn btn-secondary btn-sm" style={{textDecoration:"none"}}>Apply / View →</a>}
              </div>
            </div>
          ))}
          {filtered.length===0&&<div style={{gridColumn:"1/-1",textAlign:"center",padding:48,color:"var(--text3)",fontFamily:"var(--mono)"}}>No opportunities found.</div>}
        </div>
      )}
    </div>
  );
};

// Lightweight renderer for AI ### markdown sections
const renderAIText = (text) => {
  if (!text) return null;
  const lines = text.split('\n');
  return lines.map((line, i) => {
    if (line.startsWith('### ')) {
      return (
        <div key={i} style={{fontWeight:700,fontSize:13,color:"var(--accent)",marginTop:i>0?10:0,marginBottom:2,letterSpacing:".02em"}}>
          {line.replace('### ','')}
        </div>
      );
    }
    if (line.trim()==='') return <div key={i} style={{height:4}}/>;  
    return <div key={i} style={{fontSize:13,lineHeight:1.6,color:"inherit"}}>{line}</div>;
  });
};

// ── CHAT PAGE ─────────────────────────────────────────────────────────────────
const ChatPage = ({user}) => {
  const [messages,setMessages] = useState([{role:"ai",text:`Hey ${user.name?.split(" ")[0]||"there"} 👋 I'm CIT RISE AI — ask me anything about your score, career, skills, or what to do next.`}]);
  const [input,setInput] = useState("");
  const [loading,setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(()=>{ bottomRef.current?.scrollIntoView({behavior:"smooth"}); },[messages]);

  const send=async()=>{
    const q=input.trim();
    if(!q||loading)return;
    setInput("");
    setMessages(prev=>[...prev,{role:"user",text:q}]);
    setLoading(true);
    try{
      const d=await api("/ai/chat",{method:"POST",body:JSON.stringify({student_id:user.id||"student_demo",question:q})});
      setMessages(prev=>[...prev,{role:"ai",text:d.answer}]);
    }catch{
      setMessages(prev=>[...prev,{role:"ai",text:"Backend not reachable. Make sure it's running on port 8000."}]);
    }
    setLoading(false);
  };

  const suggestions=["How can I improve my RISE score?","What skills should I learn next?","How do I get a research internship?","Tips for my first hackathon?"];

  return (
    <div className="page" style={{display:"flex",flexDirection:"column",height:"calc(100vh - 32px)",paddingBottom:0}}>
      <div className="page-header fade-up" style={{flexShrink:0}}>
        <div className="page-title">AI Assistant</div>
        <div className="page-subtitle">Powered by Llama — knows your profile and score</div>
      </div>
      <div style={{flex:1,overflowY:"auto",marginBottom:12}}>
        {messages.map((m,i)=>(
          <div key={i} style={{display:"flex",justifyContent:m.role==="user"?"flex-end":"flex-start",marginBottom:12,animation:"fadeUp .3s ease both"}}>
            {m.role==="ai"&&<div style={{width:32,height:32,borderRadius:8,background:"linear-gradient(135deg,var(--accent2),var(--accent))",display:"flex",alignItems:"center",justifyContent:"center",fontSize:14,marginRight:10,flexShrink:0,marginTop:2}}>⚡</div>}
            <div className={m.role==="user"?"chat-bubble-user":"chat-bubble-ai"}>
              {m.role==="ai" ? renderAIText(m.text) : m.text}
            </div>
          </div>
        ))}
        {loading&&<div style={{display:"flex",alignItems:"center",gap:10,color:"var(--text3)",fontFamily:"var(--mono)",fontSize:12,marginBottom:12}}>
          <div style={{width:32,height:32,borderRadius:8,background:"linear-gradient(135deg,var(--accent2),var(--accent))",display:"flex",alignItems:"center",justifyContent:"center"}}>⚡</div>
          <span style={{animation:"pulse 1.2s infinite"}}>Thinking...</span>
        </div>}
        <div ref={bottomRef}/>
      </div>
      {messages.length===1&&(
        <div style={{display:"flex",gap:8,flexWrap:"wrap",marginBottom:10}}>
          {suggestions.map(s=><button key={s} className="btn btn-secondary btn-sm" onClick={()=>setInput(s)}>{s}</button>)}
        </div>
      )}
      <div style={{display:"flex",gap:10,paddingBottom:24,flexShrink:0}}>
        <input className="form-input" style={{flex:1}} placeholder="Ask about your career, score, skills..."
          value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==="Enter"&&send()}/>
        <button className="btn btn-primary" onClick={send} disabled={loading||!input.trim()}>
          {loading?<Spinner/>:"Send →"}
        </button>
      </div>
    </div>
  );
};

// ── NOTIFICATION BELL ─────────────────────────────────────────────────────────
const NotificationBell = ({userId, onNavigate}) => {
  const [notifs, setNotifs] = useState([]);
  const [open, setOpen] = useState(false);
  useEffect(()=>{
    if(!userId) return;
    api(`/notifications/${userId}`).then(d=>setNotifs(d.notifications||[])).catch(()=>{});
  },[userId]);
  return (
    <div style={{position:"relative"}}>
      <div onClick={()=>setOpen(!open)} style={{cursor:"pointer",position:"relative",width:32,height:32,display:"flex",alignItems:"center",justifyContent:"center",borderRadius:8,background:"var(--surface2)",border:"1px solid var(--border2)"}}>
        <span style={{fontSize:14}}>🔔</span>
        {notifs.length>0&&<div style={{position:"absolute",top:-4,right:-4,background:"var(--danger)",color:"#fff",borderRadius:"50%",width:16,height:16,fontSize:9,display:"flex",alignItems:"center",justifyContent:"center",fontFamily:"var(--mono)",fontWeight:700}}>{notifs.length}</div>}
      </div>
      {open&&(
        <div style={{position:"absolute",top:40,left:0,width:280,background:"var(--surface)",border:"1px solid var(--border)",borderRadius:12,padding:12,zIndex:200,boxShadow:"0 8px 32px rgba(0,0,0,.5)"}}>
          <div style={{fontFamily:"var(--mono)",fontSize:10,color:"var(--text3)",marginBottom:8,letterSpacing:".1em"}}>NOTIFICATIONS</div>
          {notifs.length===0?<div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text3)",padding:"8px 0"}}>All caught up!</div>:notifs.map(n=>(
            <div key={n.id} onClick={()=>{onNavigate(n.page);setOpen(false);}} style={{display:"flex",gap:10,padding:"8px 0",borderBottom:"1px solid var(--border)",cursor:"pointer"}}>
              <span style={{fontSize:18}}>{n.icon}</span>
              <div style={{flex:1}}>
                <div style={{fontSize:12,fontWeight:600,marginBottom:2}}>{n.title}</div>
                <div style={{fontSize:11,fontFamily:"var(--mono)",color:"var(--text3)",lineHeight:1.4}}>{n.message}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// ── DAILY CHALLENGE WIDGET ─────────────────────────────────────────────────────
const DailyChallengeWidget = ({userId}) => {
  const [challenge, setChallenge] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fetched, setFetched] = useState(false);

  const fetchChallenge = async () => {
    setLoading(true);
    try { const d=await api(`/ai/daily-challenge/${userId}`); setChallenge(d); } catch{}
    setLoading(false); setFetched(true);
  };

  const answer = async (letter) => {
    if(result||challenge?.answered) return;
    try { const d=await api(`/ai/daily-challenge/${userId}/answer`,{method:"POST",body:JSON.stringify({answer:letter})}); setResult(d); } catch{}
  };

  if(!fetched) return (
    <div className="card fade-up-3" style={{marginBottom:20,display:"flex",alignItems:"center",gap:14}}>
      <span style={{fontSize:24}}>⚡</span>
      <div style={{flex:1}}>
        <div style={{fontWeight:700,fontSize:14,marginBottom:2}}>Daily Challenge Ready</div>
        <div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)"}}>Answer correctly to earn +5 XP</div>
      </div>
      <button className="btn btn-primary btn-sm" onClick={fetchChallenge} disabled={loading}>{loading?<Spinner/>:"Start →"}</button>
    </div>
  );

  if(!challenge) return null;

  return (
    <div className="ai-card fade-up-3" style={{marginBottom:20}}>
      <div className="ai-label"><div className="ai-dot"/>Daily Challenge · +5 XP</div>
      <div style={{fontWeight:600,fontSize:14,marginBottom:12,lineHeight:1.5}}>{challenge.question}</div>
      {challenge.options?.map((opt,i)=>{
        const letter = String.fromCharCode(65+i);
        let bg="var(--surface2)",border="var(--border2)",color="var(--text)";
        if(result){
          if(letter===result.correct_answer){bg="rgba(16,185,129,.12)";border="var(--success)";color="var(--success)";}
          else if(letter===result.your_answer&&!result.correct){bg="rgba(239,68,68,.1)";border="var(--danger)";color="var(--danger)";}
        }
        return (
          <button key={i} disabled={!!(result||challenge.answered)} onClick={()=>answer(letter)}
            style={{display:"block",width:"100%",textAlign:"left",padding:"8px 12px",marginBottom:6,background:bg,border:`1px solid ${border}`,borderRadius:8,color,fontFamily:"var(--font)",cursor:(result||challenge.answered)?"default":"pointer",fontSize:13,transition:"all .15s"}}>
            <strong style={{fontFamily:"var(--mono)",marginRight:8}}>{letter}.</strong>{opt}
          </button>
        );
      })}
      {result&&(
        <div style={{marginTop:8}}>
          <div className={`alert ${result.correct?"alert-success":"alert-error"}`}>{result.correct?`✓ Correct! +${result.xp_earned} XP earned`:`✗ Incorrect. +${result.xp_earned} XP for trying`}</div>
          <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text2)",marginTop:6}}>{result.explanation}</div>
        </div>
      )}
      {challenge.answered&&!result&&<div className="alert alert-info">Already answered today! Come back tomorrow for a new challenge.</div>}
    </div>
  );
};

// ── LEADERBOARD PAGE ──────────────────────────────────────────────────────────
const LeaderboardPage = ({user}) => {
  const [data, setData] = useState(null);
  const [dept, setDept] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(()=>{
    setLoading(true);
    api(`/admin/leaderboard${dept?`?department=${encodeURIComponent(dept)}`:""}`)
      .then(d=>setData(d)).catch(()=>{}).finally(()=>setLoading(false));
  },[dept]);

  const rankIcon = r => r===1?"🥇":r===2?"🥈":r===3?"🥉":`#${r}`;
  const rankColor = r => r===1?"#ffd700":r===2?"#c0c0c0":r===3?"#cd7f32":"var(--text3)";

  return (
    <div className="page">
      <div className="page-header fade-up">
        <div className="page-title">🏆 Leaderboard</div>
        <div className="page-subtitle">Top innovators ranked by RISE Score</div>
      </div>
      {data?.departments?.length>0&&(
        <div className="segment fade-up-2">
          <button className={`seg-btn ${dept===""?"active":""}`} onClick={()=>setDept("")}>All Depts ({data.total_students})</button>
          {data.departments.map(d=>(
            <button key={d} className={`seg-btn ${dept===d?"active":""}`} onClick={()=>setDept(d)}>{d}</button>
          ))}
        </div>
      )}
      {loading?<Spinner/>:(
        <div className="card fade-up-3">
          <table className="table">
            <thead><tr><th>Rank</th><th>Name</th><th>Dept</th><th>RISE Score</th><th>Badge</th><th>Trend</th></tr></thead>
            <tbody>{data?.leaderboard?.map(s=>(
              <tr key={s.user_id} style={s.user_id===user.id?{background:"rgba(0,229,255,.05)"}:{}}>
                <td style={{fontFamily:"var(--mono)",fontWeight:800,fontSize:s.rank<=3?20:14,color:rankColor(s.rank)}}>{rankIcon(s.rank)}</td>
                <td>
                  <span style={{fontWeight:600}}>{s.name}</span>
                  {s.user_id===user.id&&<span className="badge badge-blue" style={{marginLeft:8}}>You</span>}
                </td>
                <td><span className="badge badge-blue">{s.department}</span></td>
                <td style={{fontFamily:"var(--mono)",color:"var(--accent)",fontWeight:700,fontSize:16}}>{s.rise_score}</td>
                <td><span className={`badge ${badgeColor(s.badge)}`}>🏅 {s.badge}</span></td>
                <td style={{fontFamily:"var(--mono)",fontSize:12}}>
                  {s.delta!==null?<span style={{color:s.delta>=0?"var(--success)":"var(--danger)"}}>{s.delta>=0?"↑":"↓"}{Math.abs(s.delta)}</span>:"—"}
                </td>
              </tr>
            ))}</tbody>
          </table>
          {(!data?.leaderboard?.length)&&<div style={{textAlign:"center",padding:40,color:"var(--text3)",fontFamily:"var(--mono)"}}>No students ranked yet.</div>}
        </div>
      )}
    </div>
  );
};

// ── ADMIN DASHBOARD ───────────────────────────────────────────────────────────
const AdminDashboard = () => {
  const [data,setData] = useState(null);
  const [insights,setInsights] = useState(null);
  const [tab,setTab] = useState("overview");
  const [loading,setLoading] = useState(true);
  const [iLoad,setILoad] = useState(false);

  useEffect(()=>{
    const load=async()=>{try{const d=await api("/admin/dashboard");setData(d);}catch{}setLoading(false);};
    load();
  },[]);

  const genInsights=async()=>{
    setILoad(true);
    try{const d=await api("/ai/admin-insights");setInsights(d.ai_insights);}catch{}
    setILoad(false);
  };

  const verify=async(id)=>{
    try{await api(`/achievements/${id}/verify`,{method:"PUT"});const d=await api("/admin/dashboard");setData(d);}catch{}
  };
  const reject=async(id)=>{
    try{await api(`/achievements/${id}/reject`,{method:"DELETE"});const d=await api("/admin/dashboard");setData(d);}catch{}
  };

  if(loading) return <div style={{padding:32}}><Spinner/></div>;

  return (
    <div className="page">
      <div className="page-header fade-up">
        <div className="page-title">Admin Dashboard</div>
        <div className="page-subtitle">CIT RISE — Research & Innovation Student Ecosystem</div>
      </div>
      <div className="tabs fade-up-2">
        {["overview","students","verify","insights"].map(t=>(
          <div key={t} className={`tab ${tab===t?"active":""}`} onClick={()=>setTab(t)}>{t[0].toUpperCase()+t.slice(1)}</div>
        ))}
      </div>

      {tab==="overview"&&data&&(
        <div className="fade-up">
          <div className="grid-4" style={{marginBottom:20}}>
            {[{l:"Students",v:data.stats?.total_students,c:"stat-accent"},{l:"Achievements",v:data.stats?.total_achievements,c:"stat-purple"},
              {l:"Pending",v:data.stats?.pending_verifications,c:"stat-amber"},{l:"Avg Score",v:data.stats?.average_rise_score,c:"stat-green"}].map(s=>(
              <div className="stat-card" key={s.l}><div className={`stat-value ${s.c}`}>{s.v??0}</div><div className="stat-label">{s.l}</div></div>
            ))}
          </div>
          {data.department_distribution&&(
            <div className="card">
              <div className="card-title">Department Distribution</div>
              <div style={{display:"flex",gap:10,flexWrap:"wrap"}}>
                {Object.entries(data.department_distribution).map(([k,v])=>(
                  <div key={k} style={{background:"var(--surface2)",border:"1px solid var(--border2)",borderRadius:8,padding:"10px 16px",textAlign:"center"}}>
                    <div style={{fontWeight:700,fontSize:20,color:"var(--accent)"}}>{v}</div>
                    <div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)",marginTop:2}}>{k}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {tab==="students"&&data&&(
        <div className="card fade-up">
          <div className="card-title">Top Innovators by RISE Score</div>
          <table className="table">
            <thead><tr><th>Name</th><th>Department</th><th>RISE Score</th><th>Badge</th><th>Actions</th></tr></thead>
            <tbody>{data.top_innovators?.map(s=>(
              <tr key={s.user_id}>
                <td style={{fontWeight:600}}>{s.name}</td>
                <td><span className="badge badge-blue">{s.department}</span></td>
                <td style={{fontFamily:"var(--mono)",color:"var(--accent)",fontWeight:700}}>{s.rise_score}</td>
                <td><span className={`badge ${badgeColor(s.badge)}`}>🏅 {s.badge}</span></td>
                <td>
                  <button className="btn btn-secondary btn-sm" onClick={()=>{
                    const val = prompt(`Enter new score for ${s.name}:`, s.rise_score);
                    if(val!==null && !isNaN(val)) {
                      api(`/users/admin/students/${s.user_id}/score`, {method:"PUT", body:JSON.stringify({rise_score: parseInt(val)})}).then(()=>window.location.reload()).catch(e=>alert(e.message));
                    }
                  }}>Edit Score</button>
                  <button className="btn btn-danger btn-sm" style={{marginLeft:8}} onClick={()=>{
                    if(window.confirm(`Delete ${s.name}?`)) {
                      api(`/users/${s.user_id}`, {method:"DELETE"}).then(()=>window.location.reload()).catch(e=>alert(e.message));
                    }
                  }}>Remove</button>
                </td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      )}

      {tab==="verify"&&data&&(
        <div className="fade-up">
          {data.pending_achievements?.length===0?(
            <div className="card" style={{textAlign:"center",padding:40,color:"var(--text3)",fontFamily:"var(--mono)"}}>✓ No pending verifications</div>
          ):(
            <div className="card">
              <div className="card-title">Pending Verifications ({data.pending_achievements?.length})</div>
              {data.pending_achievements?.map(a=>(
                <div key={a.achievement_id} style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"12px 0",borderBottom:"1px solid var(--border)"}}>
                  <div>
                    <div style={{fontWeight:600,marginBottom:4}}>{a.title}</div>
                    <div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)"}}>{a.type} · {a.student_id} · {a.date}</div>
                    {a.description&&<div style={{fontSize:12,color:"var(--text2)",marginTop:4}}>{a.description}</div>}
                  </div>
                  <div style={{display:"flex",gap:8,flexShrink:0}}>
                    <button className="btn btn-secondary btn-sm" onClick={()=>{
                      const title = prompt("Edit achievement title:", a.title);
                      if(title) api(`/achievements/${a.achievement_id}`, {method:"PUT", body:JSON.stringify({title})}).then(()=>window.location.reload()).catch(e=>alert(e.message));
                    }}>Edit</button>
                    <button className="btn btn-success btn-sm" onClick={()=>verify(a.achievement_id)}>✓ Verify</button>
                    <button className="btn btn-danger btn-sm" onClick={()=>reject(a.achievement_id)}>✗ Reject</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {tab==="insights"&&(
        <div className="fade-up">
          {!insights?(
            <div style={{textAlign:"center",padding:60}}>
              <div style={{fontSize:48,marginBottom:16}}>🧠</div>
              <div style={{fontWeight:700,fontSize:18,marginBottom:8}}>AI Talent Intelligence</div>
              <div style={{color:"var(--text3)",fontFamily:"var(--mono)",fontSize:13,marginBottom:24}}>Llama analyses all student data and generates strategic insights for NAAC/NIRF and management.</div>
              <button className="btn btn-primary" onClick={genInsights} disabled={iLoad}>
                {iLoad?<><Spinner/>Generating...</>:"Generate AI Insights"}
              </button>
            </div>
          ):(
            <div>
              <div className="ai-card" style={{marginBottom:20}}>
                <div className="ai-label"><div className="ai-dot"/>Executive Summary</div>
                <div style={{fontSize:15,lineHeight:1.7,marginBottom:12}}>{insights.executive_summary}</div>
                <div style={{display:"flex",alignItems:"center",gap:12}}>
                  <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text3)"}}>Innovation Health Score</div>
                  <div style={{fontWeight:800,fontSize:24,color:"var(--success)"}}>{insights.innovation_health_score}/100</div>
                </div>
              </div>
              <div className="grid-2" style={{marginBottom:20}}>
                <div className="card">
                  <div className="card-title">Key Insights</div>
                  {insights.key_insights?.map((i,idx)=>(
                    <div key={idx} style={{marginBottom:12,paddingBottom:12,borderBottom:"1px solid var(--border)"}}>
                      <div style={{display:"flex",justifyContent:"space-between",marginBottom:4}}>
                        <div style={{fontWeight:600,fontSize:13}}>{i.insight}</div>
                        <span className={`badge ${i.impact==="High"?"badge-red":i.impact==="Medium"?"badge-amber":"badge-green"}`}>{i.impact}</span>
                      </div>
                      <div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)"}}>{i.action}</div>
                    </div>
                  ))}
                </div>
                <div className="card">
                  <div className="card-title">Talent Segments (%)</div>
                  {Object.entries(insights.talent_segments||{}).map(([k,v])=>(
                    <div key={k} style={{marginBottom:10}}>
                      <div style={{display:"flex",justifyContent:"space-between",fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)",marginBottom:3}}>
                        <span>{k.replace(/_/g," ")}</span><span>{v}%</span>
                      </div>
                      <div style={{height:6,background:"var(--border2)",borderRadius:3}}>
                        <div style={{height:6,background:"var(--accent2)",borderRadius:3,width:`${v}%`}}/>
                      </div>
                    </div>
                  ))}
                  <div className="card-title" style={{marginTop:16}}>NAAC/NIRF</div>
                  <div style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text2)",fontStyle:"italic"}}>{insights.naac_nirf_highlight}</div>
                </div>
              </div>
              <div className="card">
                <div className="card-title">Strategic Recommendations</div>
                {insights.recommendations?.map((r,i)=>(
                  <div key={i} style={{fontFamily:"var(--mono)",fontSize:13,color:"var(--text2)",marginBottom:8,display:"flex",gap:8}}>
                    <span style={{color:"var(--accent)"}}>{i+1}.</span>{r}
                  </div>
                ))}
              </div>
              <button className="btn btn-secondary" style={{marginTop:14}} onClick={()=>setInsights(null)}>Regenerate</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// ── SUBMIT IDEA PAGE ────────────────────────────────────────────────────────
const SubmitIdeaPage = ({user}) => {
  const [tab, setTab] = useState("submit");
  const [form, setForm] = useState({title:"", description:""});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [err, setErr] = useState("");
  const [myIdeas, setMyIdeas] = useState([]);
  const [ideasLoading, setIdeasLoading] = useState(false);

  const loadMyIdeas = async () => {
    if(!user.id) return;
    setIdeasLoading(true);
    try { const d=await api(`/ideas/my-ideas?user_id=${user.id}`); setMyIdeas(d.ideas||[]); } catch{}
    setIdeasLoading(false);
  };

  useEffect(()=>{ if(tab==="my-ideas") loadMyIdeas(); },[tab]);

  const submit = async () => {
    if(!form.title||form.title.length<5){setErr("Title must be at least 5 characters.");return;}
    if(!form.description||form.description.length<20){setErr("Description must be at least 20 characters.");return;}
    setLoading(true);setErr("");setResult(null);
    try{
      const d=await api("/ideas/submit",{method:"POST",body:JSON.stringify({...form,student_id:user.id||"student_demo"})});
      setResult(d); setForm({title:"",description:""});
    }catch(e){setErr(e.message||"Submission failed.");}
    setLoading(false);
  };

  const statusColor = s=>({selected:"badge-green",rejected:"badge-red",reviewed:"badge-blue",pending:"badge-amber"}[s]||"badge-amber");

  return (
    <div className="page">
      <div className="page-header fade-up">
        <div className="page-title">Innovation Ideas</div>
        <div className="page-subtitle">Submit your startup or research idea — AI instant analysis</div>
      </div>
      <div className="segment fade-up-2">
        <button className={`seg-btn ${tab==="submit"?"active":""}`} onClick={()=>setTab("submit")}>Submit Idea</button>
        <button className={`seg-btn ${tab==="qr"?"active":""}`} onClick={()=>setTab("qr")}>Google Form</button>
        <button className={`seg-btn ${tab==="my-ideas"?"active":""}`} onClick={()=>setTab("my-ideas")}>My Ideas</button>
      </div>

      {tab==="submit"&&(
        <div className="fade-up">
          {result?(
            <div>
              <div className="alert alert-success">✓ Idea submitted! AI has analyzed it.</div>
              <div className="grid-2" style={{marginBottom:16}}>
                <div className="ai-card">
                  <div className="ai-label"><div className="ai-dot"/>AI Analysis</div>
                  <div style={{fontWeight:700,fontSize:16,marginBottom:8}}>{result.idea?.category}</div>
                  <div style={{display:"flex",gap:12,marginBottom:10}}>
                    <div className="stat-card" style={{flex:1,padding:12}}>
                      <div className="stat-value stat-accent" style={{fontSize:28}}>{result.ai_analysis?.feasibility_score}</div>
                      <div className="stat-label">Feasibility /100</div>
                    </div>
                    <div className="stat-card" style={{flex:1,padding:12}}>
                      <div className="stat-value stat-purple" style={{fontSize:18}}>{result.ai_analysis?.potential_impact}</div>
                      <div className="stat-label">Potential Impact</div>
                    </div>
                  </div>
                  <div style={{fontSize:13,color:"var(--text2)",lineHeight:1.6}}>{result.ai_analysis?.feasibility_reasoning}</div>
                </div>
                <div className="card">
                  <div className="card-title">Suggested First Steps</div>
                  {result.ai_analysis?.suggested_first_steps?.map((s,i)=>(
                    <div key={i} style={{fontFamily:"var(--mono)",fontSize:12,color:"var(--text2)",marginBottom:8,display:"flex",gap:8}}>
                      <span style={{color:"var(--accent)"}}>{i+1}.</span>{s}
                    </div>
                  ))}
                  {result.ai_analysis?.mentor_suggestions?.length>0&&<>
                    <div className="card-title" style={{marginTop:12}}>Suggested Mentors</div>
                    {result.ai_analysis.mentor_suggestions.map(m=><Tag key={m} label={m}/>)}
                  </>}
                </div>
              </div>
              <button className="btn btn-secondary" onClick={()=>setResult(null)}>Submit Another →</button>
            </div>
          ):(
            <div className="card">
              <div className="card-title">New Idea Submission</div>
              {err&&<div className="alert alert-error">{err}</div>}
              <div className="form-group">
                <label className="form-label">Idea Title *</label>
                <input className="form-input" value={form.title} onChange={e=>setForm({...form,title:e.target.value})} placeholder="e.g. AI-powered attendance system using facial recognition"/>
              </div>
              <div className="form-group">
                <label className="form-label">Description * (min 20 chars)</label>
                <textarea className="form-input" style={{minHeight:120}} value={form.description} onChange={e=>setForm({...form,description:e.target.value})} placeholder="Describe your idea — the problem it solves, how it works, and who benefits..."/>
              </div>
              <button className="btn btn-primary" onClick={submit} disabled={loading}>
                {loading?<><Spinner/> AI is analyzing...</>:"⚡ Submit & Analyze with AI"}
              </button>
            </div>
          )}
        </div>
      )}

      {tab==="qr"&&(
        <div className="grid-2 fade-up">
          <div className="card" style={{textAlign:"center",padding:"40px 20px"}}>
            <div style={{fontSize:48,marginBottom:16}}>📱</div>
            <div style={{fontWeight:700,fontSize:18,marginBottom:8}}>Scan to Submit via Google Form</div>
            <img src="/CITBIF_QR.jpeg" alt="QR Code to Form" style={{width:"100%",maxWidth:240,margin:"0 auto 20px",borderRadius:12,border:"1px solid var(--border)"}}/>
            <div style={{fontFamily:"var(--mono)",fontSize:13,color:"var(--text3)",marginBottom:20}}>Google Forms for seamless data collection.</div>
            <a href="https://scnv.io/dx3g?qr=1" target="_blank" rel="noreferrer" className="btn btn-primary" style={{textDecoration:"none"}}>Open Web Form →</a>
          </div>
          <div className="card">
            <div className="card-title">What happens next?</div>
            {[["Submit Form","Fill out the Google Form with your idea details."],["AI Analysis","Gemini automatically scores feasibility and suggests mentors."],["Admin Review","Admins review and assign RISE score boosts (+20-40 pts)."]].map(([t,d],i)=>(
              <div key={i} style={{display:"flex",gap:12,marginBottom:16}}>
                <div style={{width:28,height:28,borderRadius:14,background:"var(--surface2)",display:"flex",alignItems:"center",justifyContent:"center",fontWeight:700,color:i===2?"var(--accent)":"var(--text2)",flexShrink:0}}>{i+1}</div>
                <div><div style={{fontWeight:600,marginBottom:2}}>{t}</div><div style={{fontSize:13,color:"var(--text3)"}}>{d}</div></div>
              </div>
            ))}
          </div>
        </div>
      )}

      {tab==="my-ideas"&&(
        <div className="fade-up">
          {ideasLoading?<Spinner/>:myIdeas.length===0?(
            <div className="card" style={{textAlign:"center",padding:"48px 24px",color:"var(--text3)"}}>
              <div style={{fontSize:36,marginBottom:12}}>💡</div>
              <div style={{fontFamily:"var(--mono)",fontSize:13}}>No ideas submitted yet. Start with the Submit tab!</div>
            </div>
          ):(
            <div className="grid-2">
              {myIdeas.map(idea=>(
                <div className="card" key={idea.id}>
                  <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:8}}>
                    <div style={{fontWeight:700,fontSize:15,flex:1,marginRight:8}}>{idea.title}</div>
                    <span className={`badge ${statusColor(idea.status)}`}>{idea.status.toUpperCase()}</span>
                  </div>
                  <span className="badge badge-purple" style={{marginBottom:8,display:"inline-flex"}}>{idea.category}</span>
                  <div style={{fontSize:13,color:"var(--text2)",lineHeight:1.5,marginBottom:10}}>{idea.description.slice(0,120)}{idea.description.length>120?"...":""}</div>
                  <div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)",marginBottom:6}}>
                    Feasibility: <span style={{color:"var(--accent)"}}>{idea.feasibility_score}/100</span> · {idea.submitted_at?.slice(0,10)}
                  </div>
                  {idea.rise_score_impact>0&&<div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--success)"}}>+{idea.rise_score_impact} RISE points earned</div>}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// ── ADMIN IDEAS PAGE ────────────────────────────────────────────────────────
const AdminIdeasPage = ({user}) => {
  const [ideas, setIdeas] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef(null);
  const [msg, setMsg] = useState("");

  const load = async () => {
    try {
      const d = await api("/ideas/admin/list?limit=100");
      setIdeas(d.ideas || []);
      setStats(d.analytics);
    } catch {}
    setLoading(false);
  };
  
  useEffect(() => { load(); }, []);

  const handleImport = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true); setMsg("");
    try {
      const fd = new FormData();
      fd.append("file", file);
      const d = await apiForm("/ideas/admin/import-csv", fd);
      setMsg(d.message || "Imported successfully.");
      await load();
    } catch (err) {
      setMsg(err.message || "Import failed.");
    }
    setUploading(false);
    if(fileRef.current) fileRef.current.value = "";
  };

  const reviewIdea = async (id, status) => {
    try {
      await api(`/ideas/${id}/review`, {method:"POST", body:JSON.stringify({status})});
      await load();
    } catch (e) { alert("Failed to review: " + e.message); }
  };

  return (
    <div className="page">
      <div className="page-header fade-up" style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start"}}>
        <div><div className="page-title">Manage Ideas</div><div className="page-subtitle">Review student ideas and assign RISE scores</div></div>
        <div style={{display:"flex",gap:10}}>
          <input type="file" accept=".csv" ref={fileRef} style={{display:"none"}} onChange={handleImport}/>
          <button className="btn btn-primary" onClick={()=>fileRef.current?.click()} disabled={uploading}>
            {uploading ? <><Spinner/>Importing...</> : "📥 Import CSV"}
          </button>
        </div>
      </div>
      
      {msg && <div className="alert alert-info fade-up-2">{msg}</div>}

      {loading ? <Spinner/> : (
        <div className="grid-2 fade-up-3">
          {ideas.map(i => (
            <div className="card" key={i.id}>
              <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:8}}>
                <div>
                  <div style={{fontWeight:700,fontSize:15,marginBottom:4}}>{i.title}</div>
                  <span className={`badge ${i.status==="selected"?"badge-green":i.status==="rejected"?"badge-red":i.status==="reviewed"?"badge-blue":"badge-amber"}`}>{i.status.toUpperCase()}</span>
                  <span className="badge badge-purple" style={{marginLeft:4}}>{i.category}</span>
                </div>
              </div>
              <div style={{fontSize:13,color:"var(--text2)",lineHeight:1.5,marginBottom:10}}>{i.description}</div>
              <div style={{fontFamily:"var(--mono)",fontSize:11,color:"var(--text3)",marginBottom:12}}>
                By: {i.student_id} · AI Feasibility: {i.feasibility_score}/100
              </div>
              
              {i.mentor_suggestions?.length > 0 && (
                <div style={{marginBottom:12}}>
                  <div style={{fontSize:11,fontFamily:"var(--mono)",color:"var(--text3)",marginBottom:4}}>Suggested Mentors:</div>
                  {i.mentor_suggestions.map(m=><Tag key={m} label={m}/>)}
                </div>
              )}

              {i.status === "pending" && (
                <div style={{display:"flex",gap:8,borderTop:"1px solid var(--border)",paddingTop:12}}>
                  <button className="btn btn-secondary btn-sm" onClick={()=>{const n=prompt("Edit Title:", i.title); if(n) { api(`/ideas/${i.id}`,{method:"PUT",body:JSON.stringify({title:n})}).then(load).catch(e=>alert(e.message)) }}}>Edit</button>
                  <button className="btn btn-success btn-sm" onClick={()=>reviewIdea(i.id, "selected")}>+40pts (Select)</button>
                  <button className="btn btn-secondary btn-sm" onClick={()=>reviewIdea(i.id, "reviewed")}>+20pts (Review)</button>
                  <button className="btn btn-danger btn-sm" onClick={()=>reviewIdea(i.id, "rejected")}>Reject</button>
                </div>
              )}
              {i.status !== "pending" && (
                <div style={{display:"flex",gap:8,borderTop:"1px solid var(--border)",paddingTop:12}}>
                  <button className="btn btn-danger btn-sm" onClick={()=>{ if(window.confirm("Delete idea?")){ api(`/ideas/${i.id}`,{method:"DELETE"}).then(load).catch(e=>alert(e.message)) }}}>Delete Idea</button>
                </div>
              )}
            </div>
          ))}
          {ideas.length === 0 && <div style={{gridColumn:"1/-1",textAlign:"center",padding:48,color:"var(--text3)",fontFamily:"var(--mono)"}}>No ideas submitted yet. Import CSV to begin.</div>}
        </div>
      )}
    </div>
  );
};

// ── APP SHELL ─────────────────────────────────────────────────────────────────
const STUDENT_NAV = [
  {id:"dashboard",label:"Dashboard",icon:"⚡"},
  {id:"ai-profile",label:"AI Profile Gen",icon:"🤖"},
  {id:"score",label:"RISE Score",icon:"📊"},
  {id:"roadmap",label:"Career Roadmap",icon:"🗺️"},
  {id:"careernav",label:"CareerNav AI",icon:"🔬"},
  {id:"mentors",label:"Mentors",icon:"🤝"},
  {id:"opportunities",label:"Opportunities",icon:"🎯"},
  {id:"submit-idea",label:"Ideas",icon:"💡"},
  {id:"chat",label:"AI Assistant",icon:"💬"},
];
const ADMIN_NAV = [
  {id:"admin",label:"Admin Dashboard",icon:"🛡"},
  {id:"opportunities",label:"Opportunities",icon:"🎯"},
  {id:"admin-ideas",label:"Manage Ideas",icon:"💡"},
  {id:"mentors",label:"Mentors",icon:"🤝"},
];

export default function App() {
  const [user,setUser] = useState(null);
  const [page,setPage] = useState("dashboard");

  const handleLogin = u => {
    if(u.register){setUser({name:"New",role:"student",id:null,registering:true});setPage("register");return;}
    setUser(u); setPage(u.role==="admin"?"admin":"dashboard");
  };
  const handleLogout = () => {setUser(null);setPage("dashboard");};

  if(!user) return (<><style>{styles}</style><LoginPage onLogin={handleLogin}/></>);

  if(user.registering&&page==="register") return (
    <><style>{styles}</style>
    <RegisterPage onComplete={u=>{setUser(u);setPage("dashboard");}} onBack={()=>setUser(null)}/>
    </>
  );

  const nav = user.role==="admin"?ADMIN_NAV:STUDENT_NAV;
    const renderPage = () => {
      switch(page){
        case "dashboard":    return <StudentDashboard user={user} setPage={setPage}/>;
        case "ai-profile":   return <AIProfilePage user={user}/>;
        case "score":        return <RiseScorePage user={user}/>;
        case "roadmap":      return <CareerRoadmapPage user={user}/>;
        case "careernav":    return <CareerNavPage user={user}/>;
        case "mentors":      return <MentorsPage user={user}/>;
        case "opportunities":return user.role === "admin" ? <AdminOpportunitiesPanel user={user}/> : <OpportunitiesPage user={user}/>;
        case "submit-idea":  return <SubmitIdeaPage user={user}/>;
        case "admin-ideas":  return <AdminIdeasPage user={user}/>;
        case "chat":         return <ChatPage user={user}/>;
        case "admin":        return <AdminDashboard/>;
        default:             return <StudentDashboard user={user} setPage={setPage}/>;
      }
    };

  return (
    <><style>{styles}</style>
    <div className="app">
      <div className="sidebar">
        <div className="logo" style={{display:"flex",alignItems:"center",justifyContent:"space-between"}}>
          <div>
            <div className="logo-mark">CIT RISE</div>
            <div className="logo-sub">Innovation Platform</div>
          </div>
          {user.role==="student"&&<NotificationBell userId={user.id} onNavigate={setPage}/>}
        </div>
        <div className="nav-section">Menu</div>
        {nav.map(n=>(
          <div key={n.id} className={`nav-item ${page===n.id?"active":""}`} onClick={()=>setPage(n.id)}>
            <span className="nav-icon">{n.icon}</span>{n.label}
          </div>
        ))}
        <div className="sidebar-footer">
          <div className="user-chip">
            {user.role === "student" && user.avatar_config ? (
               <AvatarWidget config={user.avatar_config} size="32px" />
            ) : (
               <div className="avatar">{user.name?.[0]}</div>
            )}
            <div>
              <div className="user-name">{user.name}</div>
              <div className="user-role" style={{cursor:"pointer",color:"var(--danger)"}} onClick={handleLogout}>Sign out</div>
            </div>
          </div>
        </div>
      </div>
      <div className="main">{renderPage()}</div>
    </div>
    </>
  );
}
