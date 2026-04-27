import { useState, useEffect } from 'react'

// mosaic size pattern for up to N projects (repeats last entry for extras)
const SPANS = [
  { col: 2, row: 2 },
  { col: 1, row: 1 },
  { col: 1, row: 1 },
  { col: 1, row: 1 },
  { col: 2, row: 1 },
]

export default function Projects({ projects }) {
  const [selectedIdx, setSelectedIdx] = useState(null)
  const selected = selectedIdx !== null ? projects[selectedIdx] : null

  useEffect(() => {
    if (selected === null) return
    const onKey = e => { if (e.key === 'Escape') setSelectedIdx(null) }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [selected])

  useEffect(() => {
    document.body.style.overflow = selected ? 'hidden' : ''
    return () => { document.body.style.overflow = '' }
  }, [selected])

  return (
    <section className="section" id="projects">
      <div className="container">
        <div className="section-header">
          <span className="section-num">01</span>
          <span className="section-label">projects</span>
          <span className="section-title">Case Studies</span>
          <span className="section-sep" />
        </div>

        <div className="projects-mosaic">
          {projects.map((p, i) => {
            const span = SPANS[i] || { col: 1, row: 1 }
            return (
              <button
                key={p.id}
                className="project-tile"
                style={{ gridColumn: `span ${span.col}`, gridRow: `span ${span.row}` }}
                onClick={() => setSelectedIdx(i)}
                aria-label={`Ver proyecto: ${p.title}`}
              >
                {p.image && <img src={p.image} alt="" className="tile-bg" />}
                <div className="tile-veil" />
                <div className="tile-body">
                  <span className="tile-num">project_{String(i + 1).padStart(2, '0')}</span>
                  <h3 className="tile-title">{p.title}</h3>
                  <p className="tile-tagline">// {p.tagline}</p>
                  <div className="tile-stack">
                    {p.stack.slice(0, 3).map(s => <span key={s} className="badge">{s}</span>)}
                    {p.stack.length > 3 && <span className="badge badge--more">+{p.stack.length - 3}</span>}
                  </div>
                </div>
              </button>
            )
          })}
        </div>

        {selected && (
          <div className="project-lightbox" onClick={() => setSelectedIdx(null)}>
            <article className="project-panel" onClick={e => e.stopPropagation()}>
              <button className="panel-close" onClick={() => setSelectedIdx(null)}>×</button>
              {selected.image && (
                <div className="panel-image-wrap">
                  <img src={selected.image} alt={selected.title} className="panel-image" />
                </div>
              )}
              <div className="panel-body">
                <div className="panel-header">
                  <span className="tile-num">project_{String(selectedIdx + 1).padStart(2, '0')}</span>
                  <h2 className="panel-title">{selected.title}</h2>
                  <p className="panel-tagline">// {selected.tagline}</p>
                </div>
                <div className="panel-detail">
                  <div className="detail-block">
                    <label>Problem</label>
                    <p>{selected.problem}</p>
                  </div>
                  <div className="detail-block">
                    <label>Solution</label>
                    <p>{selected.solution}</p>
                  </div>
                </div>
                {selected.keyDecisions?.length > 0 && (
                  <div className="decisions">
                    <label>Key Decisions</label>
                    <ul>
                      {selected.keyDecisions.map((d, j) => <li key={j}>{d}</li>)}
                    </ul>
                  </div>
                )}
                <div className="panel-footer">
                  <div className="stack-badges">
                    {selected.stack.map(s => <span key={s} className="badge">{s}</span>)}
                  </div>
                  <div className="project-links">
                    {selected.repo && <a href={selected.repo} target="_blank" rel="noopener" className="project-link">repo →</a>}
                    {selected.demo && <a href={selected.demo} target="_blank" rel="noopener" className="project-link">demo →</a>}
                  </div>
                </div>
              </div>
            </article>
          </div>
        )}
      </div>
    </section>
  )
}
