export default function Footer({ name }) {
  return (
    <footer className="site-footer">
      <div className="container footer-inner">
        <span className="footer-text">
          <span style={{color:'var(--green)'}}>~</span> {name} &copy; {new Date().getFullYear()}
        </span>
        <span className="footer-text">
          built with React + Vite &middot; <a href="https://github.com/marquistallman">github</a>
        </span>
      </div>
    </footer>
  )
}
