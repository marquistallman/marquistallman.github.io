export default function Footer({ name }) {
  return (
    <footer className="site-footer">
      <div className="container">
        <p>
          © {new Date().getFullYear()} {name} — Made with ❤️ ·{' '}
          <a href="https://github.com/marquistallman">GitHub</a>
        </p>
      </div>
    </footer>
  )
}
