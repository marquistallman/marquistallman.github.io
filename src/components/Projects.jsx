export default function Projects({ projects }) {
  return (
    <section id="projects">
      <h3 className="section-title">Prominent Proyects</h3>
      <div className="grid projects-grid">
        {projects.map(p => (
          <article className="card" key={p.id}>
            <img className="card-img" src={p.image} alt={p.title} />
            <div className="card-body">
              <h4>{p.title}</h4>
              <p>{p.description}</p>
              <p className="muted small">{p.tags}</p>
              <div className="card-actions">
                {p.repo && <a href={p.repo} target="_blank" rel="noopener">Repo</a>}
                {p.demo && <a href={p.demo} target="_blank" rel="noopener">Demo</a>}
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
