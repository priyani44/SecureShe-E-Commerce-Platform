import React from "react";

const Header = () => {
  return (
    <header className="hero">
      <div className="updesign">
        <div className="nav-logo">
          <div className="logo"></div>
        </div>
        <div className="text">
          <p>GET YOUR AMAZING DEALS HERE!!</p>
        </div>
        <div className="nav-search">
          <input placeholder="Search product" className="search-input" />
          <div className="search-icon">
            <i className="fa-solid fa-magnifying-glass"></i>
          </div>
        </div>
        <div className="nav-about">
          <a>About Us</a>
        </div>
        <div className="nav-cart">
          <p>Returns & Orders</p>
          <i className="fa-solid fa-cart-shopping"></i>
        </div>
      </div>

      <div className="dropdown">
        <div className="dropdown-options">
          <a href="/signup.html">
            <button className="sign-up">Sign Up</button>
          </a>
          <a href="/signin.html">
            <button className="sign-up">Sign-in</button>
          </a>
        </div>
      </div>

      <div className="panel">
        <div className="panel-all">
          <i className="fa-solid fa-bars"></i>
          All
        </div>
        <div className="panelops">
          <p>Categories</p>
          <p>Brands</p>
          <p>Trending Fashion</p>
          <p>Beauty Advice</p>
        </div>
      </div>
    </header>
  );
};
export default Header;
