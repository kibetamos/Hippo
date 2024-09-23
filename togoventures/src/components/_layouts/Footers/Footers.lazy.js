import React, { lazy, Suspense } from 'react';

const LazyFooters = lazy(() => import('./Footers'));

const Footers = props => (
  <Suspense fallback={null}>
    <LazyFooters {...props} />
  </Suspense>
);

export default Footers;
