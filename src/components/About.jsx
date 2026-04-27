import { useState } from 'react'

function MetaValue({ label, value }) {
  const [toast, setToast] = useState('')

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(value)
      setToast('Copied')
    } catch {
      setToast('Copy failed')
    }
    setTimeout(() => setToast(''), 1600)
  }

  return (
    <li>
      <strong>{label}</strong>
      <span className="meta-value" onClick={handleCopy} style={{ position: 'relative' }}>
        {value}
        {toast && <span className="meta-toast visible">{toast}</span>}
      </span>
    </li>
  )
}

export default function About({ data }) {
  return (
    <section className="split" id="about">
      <div className="about-card">
        <h3 className="section-title">About me</h3>
        <p>{data.bio}</p>
        <ul className="meta-list">
          <MetaValue label="Name:"             value={data.name}   />
          <MetaValue label="Email:"            value={data.email}  />
          <MetaValue label="Discord / Telegram:" value={data.social} />
        </ul>
      </div>
      <div className="card mini-card">
        <h4>Searching</h4>
        <p>{data.searching}</p>
      </div>
    </section>
  )
}
