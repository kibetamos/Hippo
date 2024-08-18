import React, { useEffect, useState } from 'react';
import supabase from '../config/supabaseClient';
import ProductCard from './ProductCard';

export default function Home() {
  const [fetchError, setFetchError] = useState(null);
  const [products, setProducts] = useState(null);
  const [searchQuery, setSearchQuery] = useState(''); // State for search query
  const [filteredProducts, setFilteredProducts] = useState(null); // State for filtered products

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
        setFilteredProducts(data); // Set filtered products initially to all products
        setFetchError(null);
      }
    };

    fetchProducts();
  }, []);

  useEffect(() => {
    if (products) {
      const lowercasedQuery = searchQuery.toLowerCase();
      const filteredData = products.filter(product =>
        product.Name.toLowerCase().includes(lowercasedQuery)
      );
      setFilteredProducts(filteredData);
    }
  }, [searchQuery, products]); // Run this effect whenever searchQuery or products change

  return (
    <div className='page Home'>
      {fetchError && (<p>{fetchError}</p>)}

      <input
        type="text"
        placeholder="Search products..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)} // Update search query
      />

      {filteredProducts && (
        <div className='products'>
          <div className='product-grid'>
            {filteredProducts.map(product => (
              <ProductCard key={product.Id} product={product} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
