import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Footers from './Footers';

describe('<Footers />', () => {
  test('it should mount', () => {
    render(<Footers />);
    
    const footers = screen.getByTestId('Footers');

    expect(footers).toBeInTheDocument();
  });
});