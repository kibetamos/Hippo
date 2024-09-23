import React from 'react';
import PropTypes from 'prop-types';
import styles from './Footers.module.css';

const Footers = () => (
  <div className={styles.Footers} data-testid="Footers">

    <footer class="bg-secondary pt-3">
      <div class="text-center pb-3">
        <p class="mb-0">Copyright ©
          <script>var CurrentYear = new Date().getFullYear()
            document.write(CurrentYear)</script> <br /> A project by <a href="">TechVentures</a>
        </p>
      </div>
    </footer>
  </div>
);

Footers.propTypes = {};

Footers.defaultProps = {};

export default Footers;
