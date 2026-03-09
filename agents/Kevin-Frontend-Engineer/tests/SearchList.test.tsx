import React from 'react'
import { render, screen } from '@testing-library/react'
import SearchList from './SearchList'

const mockFetch = (data: any) => {
  global.fetch = jest.fn().mockResolvedValue({ ok: true, json: async () => data }) as any
}

describe('SearchList', () => {
  it('renders items and counts', async () => {
    mockFetch({ items: [{ id: '1', name: 'One' }], total_count: 1, page: 1, per_page: 20 })
    render(<SearchList query="one" />)
    expect(await screen.findByText(/Showing 1 of 1/)).toBeInTheDocument()
    expect(await screen.findByText('One')).toBeInTheDocument()
  })

  it('shows error when pagination fields missing', async () => {
    mockFetch({ foo: 'bar' })
    render(<SearchList query="xx" />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid response from server (pagination fields missing)')
  })
})
