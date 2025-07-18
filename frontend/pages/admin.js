import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'

export default function Admin() {
  const router = useRouter()
  const [picks, setPicks] = useState([])

  useEffect(() => {
    if (localStorage.getItem('xclusive_auth') !== 'true') {
      router.replace('/login')
      return
    }
    fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'}/api/todays-picks`)
      .then(r => r.json())
      .then(setPicks)
  }, [router])

  return (
    <div className="min-h-screen p-6 bg-gray-50">
      <h1 className="text-3xl font-bold mb-4">Xclusive Admin Panel</h1>
      <p>This is where you’ll manage picks, exports, and more.</p>
      <ul className="mt-4">
        {picks.map(p => (
          <li key={p.id} className="mb-2">
            {p.matchup} — Confidence: {p.confidence_score}%, Win%: {p.win_probability}%
          </li>
        ))}
      </ul>
    </div>
  )
}
