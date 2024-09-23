// import React, { useState, useEffect } from "react";
// import PropTypes from 'prop-types';
// import supabase from "../../config/supabaseClient";
// import Header from '../../_layouts/Headers/Headers';
// import Sidebar from '../../_layouts/Sidebar/Sidebar';
// import Footer from '../../_layouts/Footers/Footers';
// import styles from '/home/amos/Documents/projects/Hippo/togoventures/src/components/Pages/products/Home.module.css';


// const Search2 = () => {
//   const [products, setProducts] = useState([]);
//   const [fetchError, setFetchError] = useState(null);
//   const [nameFilter, setNameFilter] = useState('');
//   const [brandFilter, setBrandFilter] = useState('');
//   const [categoryFilter, setCategoryFilter] = useState('');
//   const [modelFilter, setModelFilter] = useState('');
//   const [skuFilter, setSkuFilter] = useState('');

//   useEffect(() => {
//     const fetchProducts = async () => {
//       const { data, error } = await supabase
//         .from('commerce')
//         .select();

//       if (error) {
//         setFetchError('Could not fetch the data');
//         setProducts([]);
//         console.log(error);
//       }

//       if (data) {
//         setProducts(data);
//         setFetchError(null);
//       }
//     };

//     fetchProducts();
//   }, []);

//   const truncateString = (str, num = 50) => {
//     if (str.length > num) {
//       return str.slice(0, num) + '...';
//     } else {
//       return str;
//     }
//   };

//   const capitalizeFirstLetter = (str) => {
//     return str.charAt(0).toUpperCase() + str.slice(1);
//   };

//   const filteredProducts = products.filter(product =>
//     (!nameFilter || product.Name.toLowerCase().includes(nameFilter.toLowerCase())) &&
//     (!brandFilter || product.Brand?.toLowerCase().includes(brandFilter.toLowerCase())) &&
//     (!categoryFilter || product['Category 1']?.toLowerCase().includes(categoryFilter.toLowerCase())) &&
//     (!modelFilter || product.Model?.toLowerCase().includes(modelFilter.toLowerCase())) &&
//     (!skuFilter || product.SKU_code?.toLowerCase().includes(skuFilter.toLowerCase()))
//   );

//   return (
//     <div className={styles.Home}>
//       <Header title="Search Products"></Header>
//       <Sidebar />

//       <div className="content-body">
//         <div className="container-fluid">
//           <div className="d-flex mb-3">
//         <input
//           type="text"
//           className="form-control"
//           placeholder="Search by Name..."
//           value={nameFilter}
//           onChange={(e) => setNameFilter(e.target.value)}
//         />
//         <input
//           type="text"
//           className="form-control"
//           placeholder="Search by Brand..."
//           value={brandFilter}
//           onChange={(e) => setBrandFilter(e.target.value)}
//         />
//         <input
//           type="text"
//           className="form-control"
//           placeholder="Search by Category..."
//           value={categoryFilter}
//           onChange={(e) => setCategoryFilter(e.target.value)}
//         />
//         <input
//           type="text"
//           className="form-control"
//           placeholder="Search by Model..."
//           value={modelFilter}
//           onChange={(e) => setModelFilter(e.target.value)}
//         />
//         <input
//           type="text"
//           className="form-control"
//           placeholder="Search by SKU..."
//           value={skuFilter}
//           onChange={(e) => setSkuFilter(e.target.value)}
//         />
//       </div>

//       <table className="table table-striped">
//         <thead>
//           <tr>
//             <th>Name</th>
//             <th>Price</th>
//             {/* <th>MRP</th> */}
//             {/* <th>Discount</th> */}
//             <th>Brand</th>
//             <th>Category</th>
//             {/* <th>Model</th> */}
//             <th>Link</th>
//             <th>SKU</th>
//           </tr>
//         </thead>
//         <tbody>
//           {filteredProducts.map(product => (
//             <tr key={product.Id}>
//               <td>{truncateString(capitalizeFirstLetter(product.Name))}</td>
//               <td>{product.Price}</td>
//               {/* <td>{product.Mrp ? product.Mrp : 'N/A'}</td> */}
//               {/* <td>{product.Discount}</td> */}
//               <td>{product.Brand}</td>
//               <td>{product['Category 1']}</td>
//               {/* <td>{product.Model}</td> */}
//               <td>
//                 {product.Link ? (
//                   <a href={product.Link} target="_blank" rel="noopener noreferrer">
//                     {truncateString(product.Link)}
//                   </a>
//                 ) : 'N/A'}
//               </td>
//               <td>{product.SKU_code}</td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//     </div>
//     </div>
//   );
// };

// export default Search2;





import React, { useState, useEffect, useMemo } from "react";
import PropTypes from 'prop-types';
import supabase from "../../config/supabaseClient";
import Header from '../../_layouts/Headers/Headers';
import Sidebar from '../../_layouts/Sidebar/Sidebar';
import Footer from '../../_layouts/Footers/Footers';
import { Modal, Button } from 'react-bootstrap';
import styles from '/home/amos/Documents/projects/Hippo/togoventures/src/components/Pages/products/Home.module.css';

const Search2 = () => {
  const [products, setProducts] = useState([]);
  const [fetchError, setFetchError] = useState(null);
  const [nameFilter, setNameFilter] = useState('');
  const [brandFilter, setBrandFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [modelFilter, setModelFilter] = useState('');
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showSummary, setShowSummary] = useState(false);
  const [productsLoaded, setProductsLoaded] = useState(false); // Track if products are loaded or searched

  useEffect(() => {
    const fetchProducts = async () => {
      const { data, error } = await supabase
        .from('commerce')
        .select();

      if (error) {
        setFetchError('Could not fetch the data');
        setProducts([]);
        console.log(error);
      } else {
        setProducts(data);
        setFetchError(null);
        setProductsLoaded(true); // Products have been loaded
      }
    };

    fetchProducts();
  }, []);

  const truncateString = (str, num = 50) => {
    if (str?.length > num) {
      return str.slice(0, num) + '...';
    } else {
      return str;
    }
  };

  const capitalizeFirstLetter = (str) => {
    return str ? str.charAt(0).toUpperCase() + str.slice(1) : '';
  };

  const filteredProducts = useMemo(() => {
    return products.filter(product =>
      (!nameFilter || product.Name.toLowerCase().includes(nameFilter.toLowerCase())) &&
      (!brandFilter || product.Brand?.toLowerCase().includes(brandFilter.toLowerCase())) &&
      (!categoryFilter || product['Category 1']?.toLowerCase().includes(categoryFilter.toLowerCase())) &&
      (!modelFilter || product.Model?.toLowerCase().includes(modelFilter.toLowerCase()))
    );
  }, [products, nameFilter, brandFilter, categoryFilter, modelFilter]);

  const handleCheckboxChange = (productId) => {
    setSelectedProduct(prevSelectedProduct =>
      prevSelectedProduct === productId ? null : productId
    );
  };

  const handleShowSummary = () => {
    setShowSummary(true);
  };

  const handleCloseSummary = () => {
    setShowSummary(false);
  };

  const selectedProductData = products.find(product => product.Id === selectedProduct);

  return (
    <div className={styles.Home}>
      <Header title="Search Products" />
      <Sidebar />

      <div className="content-body">
        <div className="container-fluid">
          <div className="d-flex mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Search by Name..."
              value={nameFilter}
              onChange={(e) => setNameFilter(e.target.value)}
            />
            <input
              type="text"
              className="form-control"
              placeholder="Search by Brand..."
              value={brandFilter}
              onChange={(e) => setBrandFilter(e.target.value)}
            />
            <input
              type="text"
              className="form-control"
              placeholder="Search by Category..."
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
            />
            <input
              type="text"
              className="form-control"
              placeholder="Search by Model..."
              value={modelFilter}
              onChange={(e) => setModelFilter(e.target.value)}
            />
          </div>

          {fetchError && <p className="text-danger">{fetchError}</p>}

          {/* Show table only if products have been loaded and there is a search query */}
          {(productsLoaded && (nameFilter || brandFilter || categoryFilter || modelFilter)) && (
            <>
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Select</th>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Brand</th>
                    <th>Category</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredProducts.length > 0 ? (
                    filteredProducts.map(product => (
                      <tr key={product.Id}>
                        <td>
                          <input
                            type="checkbox"
                            checked={selectedProduct === product.Id}
                            onChange={() => handleCheckboxChange(product.Id)}
                          />
                        </td>
                        <td>{truncateString(capitalizeFirstLetter(product.Name))}</td>
                        <td>{product.Price}</td>
                        <td>{product.Brand}</td>
                        <td>{product['Category 1']}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="5">No products found</td>
                    </tr>
                  )}
                </tbody>
              </table>

              <Button
                className="btn btn-primary mt-3"
                onClick={handleShowSummary}
                disabled={!selectedProduct}
              >
                Show Summary
              </Button>

              {/* Modal Component */}
              <Modal show={showSummary} onHide={handleCloseSummary} size="lg">
                <Modal.Header closeButton>
                  <Modal.Title>Selected Product Summary</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                  {selectedProductData && (
                    <ul>
                      <li><strong>Name:</strong> {selectedProductData.Name}</li>
                      <li><strong>Price:</strong> {selectedProductData.Price}</li>
                      <li><strong>Brand:</strong> {selectedProductData.Brand}</li>
                      <li><strong>Category:</strong> {selectedProductData['Category 1']}</li>
                      <li><strong>Model:</strong> {selectedProductData.Model}</li>
                    </ul>
                  )}
                </Modal.Body>
                <Modal.Footer>
                  <Button variant="secondary" onClick={handleCloseSummary}>Close</Button>
                </Modal.Footer>
              </Modal>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

Search2.propTypes = {
  products: PropTypes.array,
  fetchError: PropTypes.string,
  nameFilter: PropTypes.string,
  brandFilter: PropTypes.string,
  categoryFilter: PropTypes.string,
  modelFilter: PropTypes.string,
};

export default Search2;
