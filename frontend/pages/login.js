import { useState } from 'react'
import { useRouter } from 'next/router'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const router = useRouter()

  const handleSubmit = e => {
    e.preventDefault()
    if (username === 'admin' && password === 'password') {
      localStorage.setItem('xclusive_auth', 'true')
      router.push('/admin')
    } else {
      setError('Invalid credentials')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded shadow-md w-full max-w-sm">
        <h1 className="text-2xl mb-6 text-center">Admin Login</h1>
        {error && <div className="mb-4 text-red-600 text-sm">{error}</div>}
        <div className="mb-4">
          <label className="block mb-1 font-medium">Username</label>
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            className="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
            required
          />
        </div>
        <div className="mb-6">
          <label className="block mb-1 font-medium">Password</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="w-full px-3 py-2 border rounded focus:outline-none focus:ring"
            required
          />
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
          Log In
        </button>
      </form>
    </div>
  )
}
