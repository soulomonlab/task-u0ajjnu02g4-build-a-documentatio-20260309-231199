import React, { useEffect, useState } from 'react'
import { fetchWithRetries } from './apiClient'
import type { PaginatedResponse } from './types'

interface Item { id: string; name: string }

interface Props {
  query: string
  page?: number
  perPage?: number
}

export const SearchList: React.FC<Props> = ({ query, page = 1, perPage = 20 }) => {
  const [data, setData] = useState<PaginatedResponse<Item> | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      setError(null)
      try {
        const res = await fetchWithRetries<PaginatedResponse<Item>>(`/api/search?q=${encodeURIComponent(query)}&page=${page}&per_page=${perPage}`)
        if (cancelled) return
        // validate pagination shape
        if (typeof res.total_count !== 'number' || !Array.isArray(res.items)) {
          setError('Invalid response from server (pagination fields missing)')
          return
        }
        setData(res)
      } catch (err: any) {
        setError(err.message || 'Network error')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [query, page, perPage])

  if (loading) return <div>Loading...</div>
  if (error) return <div role="alert">{error}</div>
  if (!data) return <div>No results</div>

  return (
    <div>
      <div>Showing {data.items.length} of {data.total_count}</div>
      <ul>
        {data.items.map((it) => (
          <li key={it.id}>{it.name}</li>
        ))}
      </ul>
    </div>
  )
}

export default SearchList
