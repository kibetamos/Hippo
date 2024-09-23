import React, { useState, useEffect } from "react";
import PropTypes from 'prop-types';

import Header from '../../_layouts/Headers/Headers';
import Sidebar from '../../_layouts/Sidebar/Sidebar';
import Footer from '../../_layouts/Footers/Footers';
import styles from '/home/amos/Documents/projects/Hippo/togoventures/src/components/Pages/products/Home.module.css';
import supabase from "../../config/supabaseClient";

const capitalizeFirstLetter = (string) => {
  if (!string) return '';
  return string.charAt(0).toUpperCase() + string.slice(1);
};

const smallLetter = (string) => {
  if (!string) return '';
  return string.charAt(0).toLowerCase() + string.slice(1);
};

const truncateString = (string, length = 20) => {
  if (!string) return '';
  return string.length > length ? `${string.slice(0, length)}...` : string;
};

export default function Products() {
  const [fetchError, setFetchError] = useState(null);
  const [products, setProducts] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const { data, error } = await supabase
          .from('commerce')
          .select();

        if (error) throw error;

        setProducts(data);
      } catch (error) {
        setFetchError('Could not fetch the data');
        setProducts([]);
        console.error(error);
      }
    };

    fetchProducts();
  }, []);

  const filteredAndSortedProducts = products
    .filter(product =>
      product.Name.toLowerCase().includes(searchQuery.toLowerCase())
    )
    .sort((a, b) => {
      if (a.Mrp && !b.Mrp) return -1;
      if (!a.Mrp && b.Mrp) return 1;
      return 0;
    });

  const totalProducts = filteredAndSortedProducts.length;

  return (
    <div className={styles.Home} data-testid="Home">
      <Header title="Dashboard" />
      <Sidebar />

      <div className="content-body">
        <div className="container-fluid">
          <div className="modal fade" id="addOrderModalside">
            <div className="modal-dialog" role="document">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">Add Event</h5>
                  <button type="button" className="close" data-dismiss="modal"><span>&times;</span></button>
                </div>
                <div className="modal-body">
                  <form>
                    <div className="form-group">
                      <label className="text-black font-w500">Event Name</label>
                      <input type="text" className="form-control" />
                    </div>
                    <div className="form-group">
                      <label className="text-black font-w500">Event Date</label>
                      <input type="date" className="form-control" />
                    </div>
                    <div className="form-group">
                      <label className="text-black font-w500">Description</label>
                      <input type="text" className="form-control" />
                    </div>
                    <div className="form-group">
                      <button type="button" className="btn btn-primary">Create</button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
          <div className="d-flex flex-wrap mb-2 align-items-center justify-content-between">
            <div className="mb-3 mr-3">
              <h6 className="fs-16 text-black font-w600 mb-0">{totalProducts} Products</h6>
              <span className="fs-14">Based on your preferences</span>
            </div>
            <div className="event-tabs mb-3 mr-3">
              <ul className="nav nav-tabs" role="tablist">
                <li className="nav-item">
                  <a className="nav-link active" data-toggle="tab" href="#All" role="tab" aria-selected="true">All</a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" data-toggle="tab" href="#Sold" role="tab" aria-selected="false">Sold</a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" data-toggle="tab" href="#Refunded" role="tab" aria-selected="false">Refunded</a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" data-toggle="tab" href="#Canceled" role="tab" aria-selected="false">Canceled</a>
                </li>
              </ul>
            </div>
            <div className="d-flex mb-3">
              <select className="form-control style-2 default-select mr-3">
                <option>Newest</option>
                <option>Monthly</option>
                <option>Weekly</option>
              </select>
              <a href="javascript:void(0)" className="btn btn-primary text-nowrap">
                <i className="fa fa-file-text scale5 mr-3" aria-hidden="true"></i>Generate Report
              </a>
            </div>
          </div>
          <div className="row">
            <div className="col-xl-12">
              <div className="tab-content">
                <div id="All" className="tab-pane active fade show">
                  <div className="table-responsive">
                    <table id="example2" className="table card-table display dataTablesCard">
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
                        {filteredAndSortedProducts.map(product => (
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
                <div id="Sold" className="tab-pane fade">
                  <div className="table-responsive">
                    <table id="example3" className="table card-table display dataTablesCard">
                      <thead>
                        <tr>
                          <th>Order ID</th>
                          <th>Date</th>
                          <th>Event Name</th>
                          <th>Customer</th>
                          <th>Location</th>
                          <th>Sold Ticket</th>
                          <th>Available</th>
                          <th>Refund</th>
                          <th>Total Revenue</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>#0012451</td>
                          <td>04/08/2020<br />12:34 AM</td>
                          <td><span className="text-nowrap">The Story of Danau Toba<br /> (Musical Drama)</span></td>
                          <td>Bella Simatupang</td>
                          <td>London, US</td>
                          <td>1 Pcs</td>
                          <td>567k left</td>
                          <td><strong className="text-black">NO</strong></td>
                          <td><a href="javascript:void(0)" className="btn btn-primary btn-sm light">$125,70</a></td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}

Products.propTypes = {
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
  totalProducts: PropTypes.number,
};

Products.defaultProps = {
  fetchError: null,
  products: [],
  searchQuery: '',
  totalProducts: 0,
};
