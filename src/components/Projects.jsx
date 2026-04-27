export default function Projects({ projects }) {
  return (
    <section className="section" id="projects">
      <div className="container">
        <div className="section-header">
          <span className="section-num">01</span>
          <span className="section-label">projects</span>
          <span className="section-title">Case Studies</span>
          <span className="section-sep" />
        </div>
        <div className="projects-list">
          {projects.map((p, i) => (
            <article className="project-card" key={p.id}>
              <div className="project-num">project_{String(i + 1).padStart(2, "0")}</div>
              <h3 className="project-title">{p.title}</h3>
              <p className="project-tagline">// {p.tagline}</p>

              <div className="project-detail">
                <div className="detail-block">
                  <label>Problem</label>
                  <p>{p.problem}</p>
                </div>
                <div className="detail-block">
                  <label>Solution</label>
                  <p>{p.solution}</p>
                </div>
              </div>

              {p.keyDecisions && p.keyDecisions.length > 0 && (
                <div className="decisions">
                  <label>Key Decisions</label>
                  <ul>
                    {p.keyDecisions.map((d, j) => <li key={j}>{d}</li>)}
                  </ul>
                </div>
              )}

              {p.image && (
                <div className="project-image-wrap">
                  <img src={p.image} alt={p.title} className="project-image" />
                </div>
              )}

              <div className="project-footer">
                <div className="stack-badges">
                  {p.stack.map(s => <span key={s} className="badge">{s}</span>)}
                </div>
                <div className="project-links">
                  {p.repo && <a href={p.repo} target="_blank" rel="noopener" className="project-link">repo &rarr;</a>}
                  {p.demo && <a href={p.demo} target="_blank" rel="noopener" className="project-link">demo &rarr;</a>}
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
