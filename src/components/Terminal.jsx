import { useState, useRef, useEffect } from 'react'

export default function Terminal({ data, open, onClose }) {
  const [history, setHistory] = useState([
    { type: 'success', text: 'Portfolio terminal v1.0 — type "help" for commands.' },
  ])
  const [input, setInput]         = useState('')
  const [cmdHistory, setCmdHistory] = useState([])
  const [histIdx, setHistIdx]     = useState(-1)
  const outputRef = useRef(null)
  const inputRef  = useRef(null)

  useEffect(() => {
    if (open && inputRef.current) inputRef.current.focus()
  }, [open])

  useEffect(() => {
    if (outputRef.current)
      outputRef.current.scrollTop = outputRef.current.scrollHeight
  }, [history])

  const addLines = (lines) => setHistory(prev => [...prev, ...lines])

  const process = (cmd) => {
    const raw = cmd.trim()
    if (!raw) return
    const lines = [{ type: 'input', text: raw }]

    switch (raw.toLowerCase()) {
      case 'help':
        lines.push(
          { type: 'info',   text: 'Commands:' },
          { type: 'output', text: '  projects  — list all projects' },
          { type: 'output', text: '  lab       — show experiments' },
          { type: 'output', text: '  skills    — show skills by category' },
          { type: 'output', text: '  about     — about me' },
          { type: 'output', text: '  contact   — contact info' },
          { type: 'output', text: '  clear     — clear output' },
        )
        break

      case 'projects':
      case 'ls projects':
        data.projects.forEach((p, i) => {
          lines.push({ type: 'info',   text: `[${i + 1}] ${p.title}` })
          lines.push({ type: 'output', text: `    // ${p.tagline}` })
          lines.push({ type: 'output', text: `    stack: ${p.stack.join(', ')}` })
          if (p.repo) lines.push({ type: 'output', text: `    repo:  ${p.repo}` })
        })
        break

      case 'lab':
      case 'experiments':
        data.experiments.forEach(e => {
          lines.push({ type: 'info',   text: `[${e.status}] ${e.title}` })
          lines.push({ type: 'output', text: `    ${e.description}` })
        })
        break

      case 'skills':
        Object.entries(data.skills).forEach(([cat, list]) => {
          lines.push({ type: 'info',   text: `${cat}:` })
          lines.push({ type: 'output', text: `  ${list.join(', ')}` })
        })
        break

      case 'about':
        lines.push({ type: 'output', text: data.about.bio })
        lines.push({ type: 'info',   text: `interests: ${data.about.interests.join(', ')}` })
        break

      case 'contact':
        data.contact.forEach(c => {
          lines.push({ type: 'output', text: `${c.label}  →  ${c.href}` })
        })
        break

      case 'clear':
        setHistory([])
        return

      default:
        lines.push({ type: 'error', text: `command not found: ${raw}. Try "help".` })
    }

    addLines(lines)
    setCmdHistory(prev => [raw, ...prev])
    setHistIdx(-1)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      process(input)
      setInput('')
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      const next = Math.min(histIdx + 1, cmdHistory.length - 1)
      setHistIdx(next)
      setInput(cmdHistory[next] || '')
    } else if (e.key === 'ArrowDown') {
      e.preventDefault()
      const next = Math.max(histIdx - 1, -1)
      setHistIdx(next)
      setInput(next === -1 ? '' : cmdHistory[next])
    } else if (e.key === 'Escape') {
      onClose()
    }
  }

  return (
    <div className={`terminal-panel${open ? ' open' : ''}`}>
      <div className="terminal-titlebar">
        <div className="terminal-title">
          <div className="traffic-lights">
            <span className="tl-red"    style={{ cursor: 'pointer' }} onClick={onClose} />
            <span className="tl-yellow" />
            <span className="tl-green"  />
          </div>
          portfolio — bash
        </div>
        <button className="terminal-close" onClick={onClose}>×</button>
      </div>

      <div className="terminal-output" ref={outputRef}>
        {history.map((line, i) => (
          <div key={i} className={`t-${line.type}`}>
            {line.type === 'input' && <span className="t-prompt">❯ </span>}
            {line.text}
          </div>
        ))}
      </div>

      <div className="terminal-input-row">
        <span className="t-prompt">❯</span>
        <input
          ref={inputRef}
          className="terminal-input"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="type a command…"
          spellCheck={false}
          autoComplete="off"
        />
      </div>
    </div>
  )
}
