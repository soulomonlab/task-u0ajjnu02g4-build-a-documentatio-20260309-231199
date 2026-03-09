import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import LoginForm from './LoginForm'
import * as api from './apiClient'

describe('LoginForm', () => {
  it('shows validation error when fields empty', async () => {
    render(<LoginForm />)
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }))
    expect(await screen.findByRole('alert')).toHaveTextContent('Email and password are required')
  })

  it('calls setTokens on successful login', async () => {
    const fakeSetTokens = jest.spyOn(api, 'setTokens')
    global.fetch = jest.fn().mockResolvedValueOnce({ ok: true, json: async () => ({ access_token: 'a', refresh_token: 'r', expires_in: 3600 }) }) as any
    render(<LoginForm />)
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'a@b.com' } })
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'pw' } })
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }))
    await waitFor(() => expect(fakeSetTokens).toHaveBeenCalled())
    fakeSetTokens.mockRestore()
  })
})
