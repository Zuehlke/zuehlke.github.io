import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders landing page, Zühlke claim', () => {
  render(<App />);
  const linkElement = screen.getByText(/Producing cool, innovative solutions and solving tough technical problems is what Zühlke lives for/i);
  expect(linkElement).toBeInTheDocument();
});
