import Header   from './components/Header'
import Hero     from './components/Hero'
import Projects from './components/Projects'
import About    from './components/About'
import Skills   from './components/Skills'
import Contact  from './components/Contact'
import Footer   from './components/Footer'
import data     from './data/portfolio.json'

export default function App() {
  return (
    <>
      <Header data={data.header} />
      <main className="container">
        <Hero     data={data.hero}         />
        <Projects projects={data.projects} />
        <About    data={data.about}        />
        <Skills   skills={data.skills}     />
        <Contact  contacts={data.contact}  />
      </main>
      <Footer name={data.header.name} />
    </>
  )
}
