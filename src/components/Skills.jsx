const GROUPS = [
  { key: "backend", label: "Backend",          dot: "blue"  },
  { key: "systems", label: "Systems & DevOps", dot: "green" },
  { key: "tools",   label: "Tools & Misc",     dot: "red"   },
]

export default function Skills({ skills }) {
  return (
    <section className="section" id="skills">
      <div className="container">
        <div className="section-header">
          <span className="section-num">04</span>
          <span className="section-label">skills</span>
          <span className="section-title">Stack & Tooling</span>
          <span className="section-sep" />
        </div>
        <div className="skills-grid">
          {GROUPS.map(g => (
            <div className="skill-group" key={g.key}>
              <div className="skill-group-header">
                <span className={`skill-dot ${g.dot}`} />
                <span className="skill-group-name">{g.label}</span>
              </div>
              <div className="skill-group-body">
                {(skills[g.key] || []).map(s => (
                  <span key={s} className={`skill-tag skill-tag--${g.dot}`}>{s}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
