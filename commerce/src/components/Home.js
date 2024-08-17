import React, { useEffect, useState } from 'react';
import supabase from '../config/supabaseClient';
import ProductCard from './ProductCard';

export default function Home() {
  const [fetchError, setFetchError] = useState(null);
  const [products, setProducts] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      const { data, error } = await supabase
        .from('commerce')
        .select();

      if (error) {
        setFetchError('Could not fetch the data');
        setProducts(null);
        console.log(error);
      }

      if (data) {
        setProducts(data);
        setFetchError(null);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div className='page Home'>
      {fetchError && (<p>{fetchError}</p>)}

      {products && (
        <div className='products'>
          <div className='product-grid'>
            {products.map(product => (
              <ProductCard key={product.Id} product={product} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
