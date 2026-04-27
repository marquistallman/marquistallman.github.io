import { useState, useCallback } from 'react'

export default function Skills({ skills }) {
  const [preview, setPreview] = useState(null)
  const [pos, setPos]         = useState({ top: 0, left: 0 })

  const handleEnter = useCallback((skill, e) => {
    if (!skill.img) return
    const rect = e.currentTarget.getBoundingClientRect()
    setPos({
      top:  rect.top  - 212,
      left: Math.max(8, rect.left + rect.width / 2 - 150),
    })
    setPreview(skill)
  }, [])

  return (
    <section id="skills">
      <h3 className="section-title">Skills</h3>
      <div className="chips">
        {skills.map(s => (
          <span
            key={s.name}
            className="chip"
            title={s.name}
            onMouseEnter={e => handleEnter(s, e)}
            onMouseLeave={() => setPreview(null)}
          >
            {s.name}
          </span>
        ))}
      </div>

      {preview && (
        <div
          className="skill-preview visible"
          style={{ position: 'fixed', top: pos.top, left: pos.left, pointerEvents: 'none' }}
        >
          <img src={preview.img} alt="skill preview" />
          <div className="caption">
            <div className="title">{preview.name}</div>
            <div className="desc">{preview.desc}</div>
          </div>
        </div>
      )}
    </section>
  )
}
