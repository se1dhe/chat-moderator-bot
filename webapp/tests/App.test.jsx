import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../src/App';
import { MemoryRouter } from 'react-router-dom';

describe('App component', () => {
  it('renders without crashing', () => {
    // MemoryRouter is needed because App likely uses React Router
    const { container } = render(
      <MemoryRouter>
        <App />
      </MemoryRouter>
    );
    expect(container).toBeInTheDocument();
  });
});
