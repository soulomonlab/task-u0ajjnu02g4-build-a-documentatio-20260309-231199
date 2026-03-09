import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import RetryBanner from './RetryBanner';

describe('RetryBanner', () => {
  it('renders message and link, and calls onClose', () => {
    const onClose = jest.fn();
    render(<RetryBanner message="Rate limit" kbUrl="https://kb.example" onClose={onClose} />);

    expect(screen.getByText('Notice')).toBeInTheDocument();
    expect(screen.getByText('Rate limit')).toBeInTheDocument();
    expect(screen.getByText('Learn more')).toHaveAttribute('href', 'https://kb.example');

    fireEvent.click(screen.getByLabelText('Dismiss'));
    expect(onClose).toHaveBeenCalled();
  });
});
