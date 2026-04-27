const ICONS = { email: "📧", github: "🐙", discord: "💬", linkedin: "💼" }

export default function Contact({ contacts }) {
  return (
    <section className="section" id="contact">
      <div className="container">
        <div className="section-header">
          <span className="section-num">05</span>
          <span className="section-label">contact</span>
          <span className="section-title">Get In Touch</span>
          <span className="section-sep" />
        </div>
        <div className="contact-grid">
          {contacts.map((c, i) => (
            <a
              key={i}
              className="contact-item"
              href={c.href}
              target={c.href.startsWith("mailto") ? undefined : "_blank"}
              rel="noopener"
            >
              <div className="contact-icon">{ICONS[c.icon] || "🔗"}</div>
              <span className="contact-label">{c.label}</span>
            </a>
          ))}
        </div>
      </div>
    </section>
  )
}
