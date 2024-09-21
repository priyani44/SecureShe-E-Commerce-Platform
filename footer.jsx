import React from "react";

const Footer = () => {
  return (
    <footer>
      <div className="foot-panel1">Back to Top</div>
      <div className="foot-panel2">
        <ul>
          <p style={{ fontWeight: "bolder" }}>Get to Know us</p>
          <a href="#">Blog</a>
          <a href="#">About SecureShe</a>
          <a href="#">Contact Us</a>
          <a href="#">Quick Links</a>
        </ul>
        <ul>
          <p style={{ fontWeight: "bolder" }}>Inspire Me</p>
          <a href="#">Beauty Book</a>
          <a href="#">Nykaa Network</a>
          <a href="#">Buying Guides</a>
        </ul>
        <ul>
          <p style={{ fontWeight: "bolder" }}>Top categories</p>
          <a href="#">Makeup</a>
          <a href="#">Skincare</a>
          <a href="#">Haircare</a>
          <a href="#">Fragrance</a>
          <a href="#">Moms</a>
          <a href="#">Health and wellness</a>
        </ul>
        <ul>
          <p style={{ fontWeight: "bolder" }}>Help</p>
          <a href="#">Contact Us</a>
          <a href="#">Frequently Asked Questions</a>
          <a href="#">Store Locator</a>
          <a href="#">Shopping & Delivery</a>
          <a href="#">Cancellation & Returns</a>
        </ul>
      </div>
      <div className="foot-panel3">
        <div className="flogo"></div>
        <div className="smsigns">
          <p>
            Show us some <i className="fa-solid fa-heart"></i> on social media
          </p>
          <div class="signs">
            <i className="fa-brands fa-instagram"></i>
            <i className="fa-brands fa-facebook"></i>
            <i className="fa-brands fa-twitter"></i>
            <i className="fa-brands fa-youtube"></i>
            <i className="fa-brands fa-pinterest"></i>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
