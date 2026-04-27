export default function Contact({ contacts }) {
  return (
    <section id="contact">
      <h3 className="section-title">Contact</h3>
      <p>If you want to review repositories, collaborate or give me something, write me:</p>
      <div className="contact-row">
        {contacts.map((c, i) => (
          <a
            key={i}
            className="contact-card"
            href={c.href}
            target={c.href.startsWith('mailto') ? undefined : '_blank'}
            rel="noopener"
          >
            {c.label}
          </a>
        ))}
      </div>
    </section>
  )
}
