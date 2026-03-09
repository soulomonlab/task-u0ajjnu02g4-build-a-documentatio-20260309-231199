import React, { useState } from 'react'
import { setTokens } from './apiClient'
import type { TokenSet } from './types'

interface Props {
  onSuccess?: () => void
}

export const LoginForm: React.FC<Props> = ({ onSuccess }) => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    if (!email || !password) {
      setError('Email and password are required')
      return
    }
    setLoading(true)
    try {
      const res = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      if (!res.ok) {
        const body = await safeParseJson(res)
        setError(body?.message || `Login failed (${res.status})`)
        setLoading(false)
        return
      }
      const json = await res.json()
      const tokens: TokenSet = {
        access_token: json.access_token,
        refresh_token: json.refresh_token,
        expires_in: json.expires_in,
      }
      setTokens(tokens)
      onSuccess?.()
    } catch (err: any) {
      setError(err.message || 'Network error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} aria-label="login-form">
      <div>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      {error && <div role="alert" style={{ color: 'red' }}>{error}</div>}
      <button type="submit" disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</button>
    </form>
  )
}

async function safeParseJson(res: Response) {
  try {
    return await res.json()
  } catch (_) {
    return { text: await res.text() }
  }
}

export default LoginForm
