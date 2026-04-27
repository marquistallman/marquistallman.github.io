import { useState } from "react"

function MetaRow({ label, value }) {
  const [toast, setToast] = useState("")
  const copy = async () => {
    try { await navigator.clipboard.writeText(value); setToast("copied!") }
    catch { setToast("failed") }
    setTimeout(() => setToast(""), 1500)
  }
  return (
    <div className="meta-row" onClick={copy}>
      <span className="meta-key">{label}</span>
      <span className="meta-val">{value}</span>
      {toast && <span className="meta-toast visible">{toast}</span>}
    </div>
  )
}

export default function About({ data }) {
  return (
    <section className="section" id="about">
      <div className="container">
        <div className="section-header">
          <span className="section-num">03</span>
          <span className="section-label">about</span>
          <span className="section-title">Who I Am</span>
          <span className="section-sep" />
        </div>
        <div className="about-grid">
          <div className="about-card">
            <p className="about-bio">{data.bio}</p>
            <p className="interests-label">Technical Interests</p>
            <div className="interests-list">
              {data.interests.map((item, i) => (
                <span key={i} className="interest-tag">{item}</span>
              ))}
            </div>
          </div>
          <div className="meta-card">
            <div className="meta-card-header">
              <div className="traffic-lights">
                <span className="tl-red" />
                <span className="tl-yellow" />
                <span className="tl-green" />
              </div>
              david@portfolio ~ info
            </div>
            <div className="meta-body">
              <MetaRow label="name"   value={data.name}   />
              <MetaRow label="email"  value={data.email}  />
              <MetaRow label="social" value={data.social} />
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
