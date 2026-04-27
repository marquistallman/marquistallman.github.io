const STATUS_LABELS = {
  'in-progress': 'in progress',
  'exploring':   'exploring',
  'paused':      'paused',
}

export default function Experiments({ experiments }) {
  if (!experiments || experiments.length === 0) return null
  return (
    <section className="section" id="experiments">
      <div className="container">
        <div className="section-header">
          <span className="section-num">02</span>
          <span className="section-label">lab</span>
          <span className="section-title">Experiments & WIP</span>
          <span className="section-sep" />
        </div>
        <div className="experiments-grid">
          {experiments.map(exp => (
            <div className="experiment-card" key={exp.id}>
              <span className={`exp-status ${exp.status}`}>
                {STATUS_LABELS[exp.status] || exp.status}
              </span>
              <h4 className="exp-title">{exp.title}</h4>
              <p className="exp-desc">{exp.description}</p>
              <div className="stack-badges">
                {exp.stack.map(s => <span key={s} className="badge">{s}</span>)}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
