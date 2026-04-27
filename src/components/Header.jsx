export default function Header({ data }) {
  return (
    <header className="site-header">
      <div className="container header-inner">
        <div className="brand">
          <img
            className="avatar"
            src={data.avatar}
            alt="Avatar"
            onError={e => { e.target.src = 'https://via.placeholder.com/96' }}
          />
          <div>
            <h1>{data.name}</h1>
            <p className="muted">{data.subtitle}</p>
          </div>
        </div>
        <nav className="nav">
          <a href="#projects">Proyects</a>
          <a href="#about">About me</a>
          <a href="#skills">Skills</a>
          <a href="#contact">Contact</a>
        </nav>
      </div>
    </header>
  )
}
