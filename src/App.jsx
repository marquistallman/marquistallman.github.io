import { useState } from "react"
import Header      from "./components/Header"
import Hero        from "./components/Hero"
import Projects    from "./components/Projects"
import Experiments from "./components/Experiments"
import About       from "./components/About"
import Skills      from "./components/Skills"
import Contact     from "./components/Contact"
import Footer      from "./components/Footer"
import Terminal    from "./components/Terminal"
import data        from "./data/portfolio.json"

export default function App() {
  const [terminalOpen, setTerminalOpen] = useState(false)

  return (
    <>
      <Header
        data={data.header}
        onTerminalToggle={() => setTerminalOpen(o => !o)}
        terminalOpen={terminalOpen}
      />
      <Hero        data={data.hero}               />
      <Projects    projects={data.projects}       />
      <Experiments experiments={data.experiments} />
      <About       data={data.about}              />
      <Skills      skills={data.skills}           />
      <Contact     contacts={data.contact}        />
      <Footer      name={data.header.name}        />
      <Terminal
        data={data}
        open={terminalOpen}
        onClose={() => setTerminalOpen(false)}
      />
    </>
  )
}
