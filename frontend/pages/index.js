export default function Home({ picks }) {
  const [picksData, setPicksData] = React.useState([])
  React.useEffect(() => {
    fetch(process.env.NEXT_PUBLIC_API_URL + '/api/todays-picks')
      .then(res => res.json())
      .then(setPicksData)
  }, [])

  const best = picksData[0] || {}

  return (
    <main className="container mx-auto p-4">
      <header className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Today’s High-Confidence Picks</h1>
        <div>{new Date().toLocaleDateString()}</div>
      </header>
      {best.matchup && (
        <section className="mb-8">
          <div className="p-4 border-2 border-gold rounded-lg bg-black text-white">
            <h2 className="text-xl font-semibold">🔒 X’s Absolute Best Bet</h2>
            <p>{best.matchup} — Confidence: {best.confidence_score}/10 — Win: {best.win_probability}%</p>
            <p className="italic mt-2">{best.summary}</p>
          </div>
        </section>
      )}
      <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {picksData.map(p => (
          <li key={p.id} className="p-4 border rounded-lg">
            <h2 className="font-bold">{p.matchup}</h2>
            <div>Type: {p.type}</div>
            <div>Confidence: {p.confidence_score}/10</div>
            <div>Sharp %: {p.sharp_pct}% | Win %: {p.win_probability}%</div>
            <div>{p.summary}</div>
          </li>
        ))}
      </ul>
      <footer className="mt-8">
        <a href="/api/export/pdf" className="underline">Download Recap (PDF)</a>
      </footer>
    </main>