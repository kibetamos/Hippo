import React, { useState, useEffect, useMemo } from "react";
import PropTypes from "prop-types";
import supabase from "../../../config/supabaseClient";
import Header from "../../_layouts/Headers/Headers";
import Sidebar from "../../_layouts/Sidebar/Sidebar";
import Footer from "../../_layouts/Footers/Footers";
import styles from "/home/bench/Documents/projects/Python/Hippo/togoventures/src/components/Pages/products/Home.module.css";
import { Modal, Button, Form } from "react-bootstrap";
import { createClient } from "@supabase/supabase-js";
import { v4 as uuidv4 } from "uuid";

const Search2 = () => {
  const [products, setProducts] = useState([]);
  const [fetchError, setFetchError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [productsLoaded, setProductsLoaded] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [file, setFile] = useState(null);
  const [uploadError, setUploadError] = useState(null);
  const [userId, setUserId] = useState('');
  const [media, setMedia] = useState([]);

  const getUser = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (user !== null) {
        setUserId(user.id);
      } else {
        setUserId("");
      }
    } catch (e) {}
  };

  async function uploadImage(e) {
    let file = e.target.files[0];
    const { data, error } = await supabase.storage.from("uploads").upload(userId + "/" + uuidv4(), file);

    if (data) {
      getMedia();
    } else {
      console.log(error);
    }
  }

  async function getMedia() {
    const { data, error } = await supabase.storage.from("uploads").list(userId + "/", {
      limit: 10,
      offset: 0,
      sortBy: { column: "name", order: "asc" },
    });

    if (data) {
      setMedia(data);
    } else {
      console.log(71, error);
    }
  }

  const signout = async () => {
    setUserId("");
    await supabase.auth.signOut();
  };

  useEffect(() => {
    getUser();
    getMedia();
  }, [userId]);

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
        setProductsLoaded(true);
      }
    };

    fetchProducts();
  }, []);

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

  const handleCheckboxChange = (productId) => {
    setSelectedProducts((prevSelectedProducts) =>
      prevSelectedProducts.includes(productId)
        ? prevSelectedProducts.filter((id) => id !== productId)
        : [...prevSelectedProducts, productId]
    );
  };


  


  const handleShowSummary = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  const handleShowUploadModal = () => {
    setShowUploadModal(true);
  };

  const handleCloseUploadModal = () => {
    setShowUploadModal(false);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!file) return;

    const { data, error } = await supabase.storage.from("test").upload(`uploads/${file.name}`, file);

    if (error) {
      setUploadError("Error uploading file.");
      console.error("Error uploading file:", error);
    } else {
      setUploadError(null);
      handleCloseUploadModal(); // Close modal after successful upload
    }
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
  <div className="container-fluid mt-5"> {/* Added margin-top to push down */}
    <div className="mb-3">
      <input
        type="text"
        className="form-control"
        placeholder="Search by Name, Brand, Category, or Model..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
    </div>

    <Button className="btn btn-primary mt-3" onClick={handleShowUploadModal}>
      Upload File
    </Button>

    {fetchError && <p className="text-danger">{fetchError}</p>}

    {productsLoaded && searchQuery && (
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
              filteredProducts.map((product) => (
                <tr key={product.Id}>
                  <td>
                    <input
                      type="checkbox"
                      checked={selectedProducts.includes(product.Id)}
                      onChange={() => handleCheckboxChange(product.Id)}
                    />
                  </td>
                  <td>{truncateString(capitalizeFirstLetter(product.Name))}</td>
                  <td>{product.Price}</td>
                  <td>{product.Brand}</td>
                  <td>{product["Category 1"]}</td>
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
          disabled={selectedProducts.length === 0}
        >
          Show Summary
        </Button>
      </>
    )}
  </div>
</div>





      {/* Modal for showing selected products */}
      <Modal show={showModal} onHide={handleCloseModal} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Selected Products Summary</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedProductDetails.length > 0 ? (
            <>
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Brand</th>
                    <th>Category</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedProductDetails.map((product) => (
                    <tr key={product.Id}>
                      <td>{truncateString(capitalizeFirstLetter(product.Name))}</td>
                      <td>{product.Price}</td>
                      <td>{product.Brand}</td>
                      <td>{product["Category 1"]}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <h3>Model Statistics:</h3>
              <table className="table table-bordered">
                <thead>
                  <tr>
                    <th>Model</th>
                    <th>Average Price</th>
                    <th>Min Price</th>
                    <th>Max Price</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(modelStats).map(([model, stats]) => (
                    <tr key={model}>
                      <td>{model}</td>
                      <td>{stats.averagePrice.toFixed(2)}</td>
                      <td>{stats.minPrice.toFixed(2)}</td>
                      <td>{stats.maxPrice.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          ) : (
            <p>No products selected</p>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Modal for uploading file */}
      <Modal show={showUploadModal} onHide={handleCloseUploadModal}>
        <Modal.Header closeButton>
          <Modal.Title>Upload File</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group controlId="formFile" className="mb-3">
            <Form.Label>Choose a file to upload</Form.Label>
            <Form.Control type="file" onChange={handleFileChange} />
          </Form.Group>

          {uploadError && <p className="text-danger">{uploadError}</p>}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseUploadModal}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleFileUpload}>
            Upload
          </Button>
        </Modal.Footer>
      </Modal>

      <Footer />
    </div>
  );
};

Search2.propTypes = {
  input: PropTypes.any,
};

export default Search2;
