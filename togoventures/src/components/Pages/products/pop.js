import React, { useState, useEffect, useMemo } from "react";
import PropTypes from "prop-types";
import supabase from "../../../config/supabaseClient";
import Header from "../../_layouts/Headers/Headers";
import Sidebar from "../../_layouts/Sidebar/Sidebar";
import Footer from "../../_layouts/Footers/Footers";
import styles from "../../Pages/products/Home.module.css";
import { Modal, Button, Form } from "react-bootstrap";
import { v4 as uuidv4 } from 'uuid';


const Search2 = () => {
  const [userId, setUserId] = React.useState("");
  const [media, setMedia] = React.useState([]);


  const [products, setProducts] = useState([]);
  const [fetchError, setFetchError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showSummary, setShowSummary] = useState(false); // Control summary display

  useEffect(() => {
    const fetchProducts = async () => {
      const { data, error } = await supabase.from("commerce").select();

      if (error) {
        setFetchError("Could not fetch the data");
        setProducts([]);
        console.log(error);
      } else {
        setProducts(data);
        setFetchError(null);
      }
    };

    fetchProducts();
  }, []);

  const getUser = async () => {

    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (user !== null) {
        setUserId(user.id);
      } else {
        setUserId('');
      }
    } catch (e) {
    }
  }

  async function uploadImage(e) {
    let file = e.target.files[0];


    const { data, error } = await supabase
      .storage
      .from('test')
      .upload(userId + "/" + uuidv4(), file)

    if (data) {
      getMedia();

    } else {
      console.log(error);
    }
  }

  async function getMedia() {

    const { data, error } = await supabase.storage.from('test').list(userId + '/', {
      limit: 10,
      offset: 0,
      sortBy: {
        column: 'name', order:
          'asc'
      }
    });

    if (data) {
      setMedia(data);
    } else {
      console.log(71, error);
    }
  }


  useEffect(() => {
    getUser();
    getMedia();
  }, [userId])


  const truncateString = (str, num = 50) => {
    return str?.length > num ? str.slice(0, num) + "..." : str;
  };

  const capitalizeFirstLetter = (str) => {
    return str ? str.charAt(0).toUpperCase() + str.slice(1) : "";
  };

  const parsePrice = (priceStr) => {
    const cleanedPriceStr = priceStr.replace(/[^0-9.]/g, "");
    const price = parseFloat(cleanedPriceStr);
    return isNaN(price) ? 0 : price;
  };

  const filteredProducts = useMemo(() => {
    return products.filter(
      (product) =>
        (!searchQuery || product.Name.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (product.Brand?.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (product["Category 1"]?.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (product.Model?.toLowerCase().includes(searchQuery.toLowerCase()))
    );
  }, [products, searchQuery]);

  const handleButtonClick = (productId) => {
    setSelectedProducts((prevSelectedProducts) => {
      if (prevSelectedProducts.includes(productId)) {
        return prevSelectedProducts.filter((id) => id !== productId);
      }
      return [...prevSelectedProducts, productId];
    });
  };

  const handleAskForSummary = () => {
    setShowSummary(true);
  };

  const selectedProductDetails = products.filter((product) =>
    selectedProducts.includes(product.Id)
  );

  const modelStats = selectedProductDetails.reduce((acc, product) => {
    const model = product.Model;
    const price = parsePrice(product.Price);

    if (!acc[model]) {
      acc[model] = {
        prices: [],
        averagePrice: 0,
        minPrice: Infinity,
        maxPrice: -Infinity,
      };
    }
    acc[model].prices.push(price);
    acc[model].minPrice = Math.min(acc[model].minPrice, price);
    acc[model].maxPrice = Math.max(acc[model].maxPrice, price);
    acc[model].averagePrice =
      acc[model].prices.reduce((sum, p) => sum + p, 0) / acc[model].prices.length;

    return acc;
  }, {});

  return (
    <div className={styles.Home}>
      <Header title="Search Products" />
      <Sidebar />

      <div className="content-body">
        <div className="container-fluid mt-5">
          <div className="mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Search by Name, Brand, Category, or Model..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          {fetchError && <p className="text-danger">{fetchError}</p>}

          {/* Show selected products */}
          {selectedProducts.length > 0 && (
            <div>
              <h3>Selected Products</h3>
              <ul>
                {selectedProductDetails.map((product) => (
                  <li key={product.Id}>
                    {product.Name} - {product.Model}
                    <Button
                      variant="danger"
                      className="ml-3"
                      onClick={() => handleButtonClick(product.Id)}
                    >
                      Remove
                    </Button>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Only show search results if searchQuery is not empty */}
          {searchQuery && filteredProducts.length > 0 && (
            <>
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Select</th>
                    <th>Name</th>
                    <th>Brand</th>
                    <th>Model No</th>
                    <th>Category</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredProducts.map((product) => (
                    <tr key={product.Id}>
                      <td>
                        <Button
                          variant="outline-secondary"
                          onClick={() => handleButtonClick(product.Id)}
                        >
                          Select
                        </Button>
                      </td>
                      <td>{truncateString(capitalizeFirstLetter(product.Name))}</td>
                      <td>{product.Brand}</td>
                      <td>{product.Model}</td>
                      <td>{product["Category 1"]}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}

          {/* Ask for summary after products are selected */}
          {selectedProducts.length > 0 && (
            <Button className="btn btn-info mt-4" onClick={handleAskForSummary}>
              Ask for Summary
            </Button>
          )}

          {/* Upload File Button */}
          <Button className="btn btn-primary mt-4" onClick={() => setShowUploadModal(true)}>
            Upload File
          </Button>

          {/* Summary Section */}
          {showSummary && selectedProducts.length > 0 && (
            <div className="summary-section mt-4">
              <h3>Selected Products Summary</h3>
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Model Number</th>
                    <th>Average Price</th>
                    <th>Price Range</th>
                    <th>Category</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.keys(modelStats).map((model) => {
                    const firstProduct = selectedProductDetails.find(product => product.Model === model);
                    return (
                      <tr key={model}>
                        <td>{firstProduct?.Name || "N/A"}</td>
                        <td>{model}</td>
                        <td>
                          {modelStats[model]?.averagePrice
                            ? modelStats[model].averagePrice.toFixed(2)
                            : "N/A"}
                        </td>
                        <td>
                          {modelStats[model]?.minPrice === Infinity || modelStats[model]?.maxPrice === -Infinity
                            ? "N/A"
                            : `${modelStats[model].minPrice.toFixed(2)} - ${modelStats[model].maxPrice.toFixed(2)}`}
                        </td>
                        <td>{firstProduct?.["Category 1"]}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      <Footer />

      {/* File Upload Modal */}
          {/* File Upload Modal */}
          <Modal show={showUploadModal} onHide={() => setShowUploadModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Upload File</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group controlId="fileUpload">
              <Form.Label>Select a file to upload</Form.Label>
              <Form.Control type="file" onChange={(e) => uploadImage(e)} />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowUploadModal(false)}>
            Close
          </Button>
          <Button variant="primary" onClick={() => console.log('File uploaded')}>
            Upload
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

Search2.propTypes = {
  products: PropTypes.array,
};

export default Search2;
