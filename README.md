# SecureShe

**SecureShe** is an e-commerce website aimed at empowering women by providing a safe and secure platform for purchasing lifestyle and fashion products. The website emphasizes security, privacy, and a strong community vibe by offering features such as chatbot support and product recommendations, tailored specifically for women.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributors](#contributors)
- [License](#license)

## Project Overview

SecureShe is designed to provide a secure online shopping experience for women. From secure transactions to personalized product recommendations, our platform ensures privacy and an engaging experience. We aim to build a strong community where women can feel safe while shopping.

## Features

- **Secure Transactions**: All user transactions are safe and secure with no data leaks.
- **Chatbot Support**: We provide a chatbot for real-time user interaction, answering queries and enhancing user experience.
- **Product Recommendations**: Personalized product suggestions based on users’ search history.
- **Backend Management**: FastAPI is used for backend, ensuring efficient handling of data and processes.
- **Responsive Frontend**: Built with modern design principles for seamless user experience across devices.

## Technology Stack

- **Frontend**: React, CSS, JSX
- **Backend**: FastAPI, Python
- **Database**: SQLite (or other supported databases via FastAPI)
- **Machine Learning**: Python for recommendation engine
- **Chatbot**: Python-based chatbot for real-time interaction
- **Other Tools**: 
  - **Email Support**: Custom email utility for user communications (`email_utils.py`)

## Installation

### Prerequisites
- Node.js
- Python 3.x
- FastAPI

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Megha-Chakraborty/SecureShe.git
   cd SecureShe
   ```

2. Install dependencies for the backend:
   ```bash
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   npm install
   ```

4. Start the backend server:
   ```bash
   uvicorn main_backend_fastapi:app --reload
   ```

5. Start the frontend:
   ```bash
   npm run start
   ```

Usage
Once everything is installed and the servers are running:

Access the website at http://localhost:3000 to explore the SecureShe platform.
Interact with the chatbot for customer support.
Browse the shop section and receive personalized product recommendations.
API Endpoints
The backend exposes the following endpoints:

/api/recommendations: Get product recommendations.

/api/chatbot: Chatbot interaction endpoint.

/api/transactions: Endpoint for handling secure transactions.

Contributors:

Megha Chakraborty : (UI/UX Design, AI Management)

Priyani Kumari : (Frontend Development)

Twinkle Sharma : (Backend Management with FastAPI)

License:

This project is licensed under the MIT License - see the LICENSE file for details.
