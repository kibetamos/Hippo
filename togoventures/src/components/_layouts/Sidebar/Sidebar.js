import React from 'react';
import PropTypes from 'prop-types';
import {
  Link, useNavigate
} from "react-router-dom";

const isMobile = {
  Android: function () {
    return navigator.userAgent.match(/Android/i);
  },
  BlackBerry: function () {
    return navigator.userAgent.match(/BlackBerry/i);
  },
  iOS: function () {
    return navigator.userAgent.match(/iPhone|iPad|iPod/i);
  },
  Opera: function () {
    return navigator.userAgent.match(/Opera Mini/i);
  },
  Windows: function () {
    return navigator.userAgent.match(/IEMobile/i) || navigator.userAgent.match(/WPDesktop/i);
  },
  any: function () {
    return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
  }
};

const Sidebar = () => (
  <div >
  
    <div class="deznav">
      <div class="deznav-scroll">
      <a href="javascript:void(0)" class="add-menu-sidebar" data-toggle="modal"data-target="#addOrderModalside">+ ToGo</a>
        {/* <a href="javascript:void(0)" class="add-menu-sidebar" data-toggle="modal" id='sendMessageModalBtn' data-target="#sendMessageModal" > Send Message</a> */}
        <a href="javascript:void(0)" id='showGroupModalBtn' class="add-menu-sidebar d-none" data-toggle="modal" data-target="#addGroupModal" > Show Group Chooser</a>
        <a href="javascript:void(0)" id='chooseIndividualContactModalBtn' class="add-menu-sidebar d-none" data-toggle="modal" data-target="#chooseIndividualContactModal" > Show Group Chooser</a>
        <a href="javascript:void(0)" id='confirmDeleteGroupModalBtn' class="add-menu-sidebar d-none" data-toggle="modal" data-target="#confirmDeleteGroupModal" > Show Group Confirm Delete</a>
        <a href="javascript:void(0)" id='showDraftsModalBtn' class="add-menu-sidebar d-none" data-toggle="modal" data-target="#addDraftsModal" > Show draft modal </a>
        <a href="javascript:void(0)" id='showDeleteContactModalBtn' data-toggle="modal" data-target="#deleteContactModal" class="btn btn-danger shadow btn-xs sharp d-none"> Delete Single Contact </a>
        <a href="javascript:void(0)" data-toggle="modal" data-target="#editContactModalside"
          class="btn btn-primary shadow btn-xs sharp mr-1 d-none" id="showEditContactModal"  > </a>

        <ul class="metismenu" id="menu">
          <li > 
            <a href="/" class="ai-icon active" aria-expanded="false">
              <i class="flaticon-381-home-3"></i>
              <span class="nav-text">Dashboard</span>
            </a>
     
          </li>
          {/* <li >
            <a href="/products" class="ai-icon active" aria-expanded="false">
              <i class="flaticon-381-notepad-1"></i>
              <span class="nav-text"> Products</span>
            </a>

          </li> */}
{/* 
          <li >
            <a href="/Search" class="ai-icon active" aria-expanded="false">
              <i class="flaticon-381-notepad-1"></i>
              <span class="nav-text"> Search</span>
            </a>

          </li> */}
          <li >
            <a href="/Search2" class="ai-icon active" aria-expanded="false">
              <i class="flaticon-381-notepad-1"></i>
              <span class="nav-text"> Search2</span>
            </a>
          </li>

          <li >
            <a href="/pop" class="ai-icon active" aria-expanded="false">
              <i class="flaticon-381-notepad-1"></i>
              <span class="nav-text"> pop</span>
            </a>
          </li>

          <li >
            <a href="/order" class="ai-icon active" aria-expanded="false">
              <i class="flaticon-381-notepad-1"></i>
              <span class="nav-text"> MyOrders</span>
            </a>
          </li>
          
        
          <li >
            <a href="/profile" class="ai-icon active" aria-expanded="false">
              <i class="flaticon-381-user-1"></i>
              <span class="nav-text">User Profile</span>
            </a>
            {/* <ul aria-expanded="false">
							<li><a href="/profile">profile</a></li>
							<li><a href="event.html">Event</a></li>
							
						</ul> */}
          </li>
        </ul>
        <div class="copyright">
        <p><strong>TechVenture </strong> © 2024 All Rights Reserved</p> 
      </div>
      </div>
    </div>
  </div>
  
);

Sidebar.propTypes = {};

Sidebar.defaultProps = {};

export default Sidebar;
