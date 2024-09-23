import React, { useState, useEffect } from "react";
import PropTypes from 'prop-types';
import supabase from "../../config/supabaseClient";
import Header from '../../_layouts/Headers/Headers';
import Sidebar from '../../_layouts/Sidebar/Sidebar';
import Footer from '../../_layouts/Footers/Footers';
import styles from '/home/amos/Documents/projects/Hippo/togoventures/src/components/Pages/products/Home.module.css';

const capitalizeFirstLetter = (string) => {
  if (!string) return '';
  return string.charAt(0).toUpperCase() + string.slice(1);
};

const truncateString = (string, length = 20) => {
  if (!string) return '';
  return string.length > length ? `${string.slice(0, length)}...` : string;
};

export default function Search() {
  const [fetchError, setFetchError] = useState(null);
  const [products, setProducts] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchProducts = async () => {
      const { data, error } = await supabase
        .from('commerce')
        .select();

      if (error) {
        setFetchError('Could not fetch the data');
        setProducts([]);
        console.log(error);
      }

      if (data) {
        setProducts(data);
        setFetchError(null);
      }
    };

    fetchProducts();
  }, []);

  const filteredProducts = products.filter(product =>
    product.Name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className={styles.Home}>
      <Header title="Search Products"></Header>
      <Sidebar />

      <div className="content-body">
        <div className="container-fluid">
          <div className="d-flex mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Search for a product..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          {fetchError && <p>{fetchError}</p>}

          <div className="table-responsive">
            <table className="table card-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Price</th>
                  <th>Mrp</th>
                  <th>Discount</th>
                  <th>Brand</th>
                  <th>Category</th>
                  <th>Model</th>
                  <th>Link</th>
                  <th>SKU</th>
                </tr>
              </thead>
              <tbody>
                {filteredProducts.map(product => (
                  <tr key={product.Id}>
                    <td>{truncateString(capitalizeFirstLetter(product.Name))}</td>
                    <td>{product.Price}</td>
                    <td>{product.Mrp ? product.Mrp : 'N/A'}</td>
                    <td>{product.Discount}</td>
                    <td>{product.Brand}</td>
                    <td>{product['Category 1']}</td>
                    <td>{product.Model}</td>
                    <td>
                      {product.Link ? (
                        <a href={product.Link} target="_blank" rel="noopener noreferrer">
                          {truncateString(product.Link)}
                        </a>
                      ) : 'N/A'}
                    </td>
                    <td>{product.SKU_code}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  );
}

Search.propTypes = {
  fetchError: PropTypes.string,
  products: PropTypes.arrayOf(PropTypes.shape({
    Id: PropTypes.string.isRequired,
    Name: PropTypes.string.isRequired,
    Price: PropTypes.number,
    Mrp: PropTypes.number,
    Discount: PropTypes.number,
    Brand: PropTypes.string,
    'Category 1': PropTypes.string,
    Model: PropTypes.string,
    Link: PropTypes.string,
    SKU_code: PropTypes.string
  })),
  searchQuery: PropTypes.string,
};

Search.defaultProps = {
  fetchError: null,
  products: [],
  searchQuery: '',
};
