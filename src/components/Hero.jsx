export default function Hero({ data }) {
  return (
    <section className="hero">
      <div>
        <h2>{data.title}</h2>
        <p className="lead">
          {data.description}{' '}
          <a href={data.githubUrl} target="_blank" rel="noopener">
            {data.githubUrl.replace('https://', '')}
          </a>
          .
        </p>
        <div className="cta-row">
          <a className="btn" href="#projects">Watch proyects</a>
          <a className="btn ghost" href={`mailto:${data.email}`}>Send email</a>
        </div>
      </div>
      <img className="hero-img" src={data.image} alt="Código" />
    </section>
  )
}
