import { useState, useEffect } from "react"

export default function Hero({ data }) {
  const [displayed, setDisplayed] = useState("")
  const [done, setDone] = useState(false)

  useEffect(() => {
    const full = data.headline
    let i = 0
    const timer = setInterval(() => {
      if (i < full.length) {
        setDisplayed(full.slice(0, ++i))
      } else {
        setDone(true)
        clearInterval(timer)
      }
    }, 38)
    return () => clearInterval(timer)
  }, [data.headline])

  return (
    <section className="hero">
      <div className="container">
        <div className="hero-prompt">~/portfolio</div>
        <h1 className="hero-headline">
          {displayed}
          {!done && <span className="cursor" />}
        </h1>
        <p className="hero-sub">{data.subheadline}</p>
        <p className="hero-desc">{data.description}</p>
        <div className="hero-stack">
          {data.stack.map(s => (
            <span key={s} className="stack-pill">{s}</span>
          ))}
        </div>
        <div className="hero-actions">
          <a className="btn-primary" href="#projects">View Projects</a>
          <a className="btn-ghost" href={data.githubUrl} target="_blank" rel="noopener">GitHub</a>
        </div>
      </div>
    </section>
  )
}
