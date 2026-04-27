export default function Header({ data, onTerminalToggle, terminalOpen }) {
  return (
    <header className="site-header">
      <div className="container header-inner">
        <div className="brand">
          <img
            className="avatar"
            src={data.avatar}
            alt="avatar"
            onError={e => { e.target.src = 'https://via.placeholder.com/34' }}
          />
          <div>
            <span className="brand-name">{data.name}</span>
            <span className="brand-role">// {data.role}</span>
          </div>
        </div>
        <nav className="nav">
          <a href="#projects">Projects</a>
          <a href="#experiments">Lab</a>
          <a href="#about">About</a>
          <a href="#skills">Skills</a>
          <a href="#contact">Contact</a>
        </nav>
        <button
          className={`terminal-btn${terminalOpen ? ' active' : ''}`}
          onClick={onTerminalToggle}
          title="Toggle terminal"
        >
          <span>_</span> terminal
        </button>
      </div>
    </header>
  )
}
