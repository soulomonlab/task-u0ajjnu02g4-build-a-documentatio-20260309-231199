import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { KBMessageBanner, KBMessage } from './KBMessageBanner';

const sample: KBMessage = {
  id: 'kb1',
  title: 'KB Update',
  body: 'We updated the knowledge base.',
  cta: { label: 'Read more', href: '/kb/kb1' },
  severity: 'info',
};

describe('KBMessageBanner', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('renders title and body', () => {
    render(<KBMessageBanner message={sample} />);
    expect(screen.getByText('KB Update')).toBeInTheDocument();
    expect(screen.getByText('We updated the knowledge base.')).toBeInTheDocument();
  });

  it('dismisses and persists to localStorage when dismissed', () => {
    render(<KBMessageBanner message={sample} version={1} persistence="local" />);
    const btn = screen.getByRole('button', { name: /dismiss/i });
    fireEvent.click(btn);
    expect(screen.queryByText('We updated the knowledge base.')).not.toBeInTheDocument();
    expect(localStorage.getItem('kb_dismiss_kb1_v1')).toBe('dismissed');
  });

  it('calls onDismiss when server persistence is used', async () => {
    const onDismiss = jest.fn(() => Promise.resolve());
    render(<KBMessageBanner message={sample} persistence="server" onDismiss={onDismiss} />);
    const btn = screen.getByRole('button', { name: /dismiss/i });
    fireEvent.click(btn);
    expect(onDismiss).toHaveBeenCalledWith('kb1', undefined);
  });
});
