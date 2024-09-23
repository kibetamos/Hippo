import React, { lazy, Suspense } from 'react';

const LazyHeaders = lazy(() => import('./Headers'));

const Headers = props => (
  <Suspense fallback={null}>
    <LazyHeaders {...props} />
  </Suspense>
);

export default Headers;
