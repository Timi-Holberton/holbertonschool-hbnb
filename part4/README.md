# HBnB - Part 4: Simple Web Client

## Description

This fourth part of the **HBnB project** introduces a front-end interface to interact with the back-end services developed in the previous stages. It leverages modern web technologies such as **HTML5**, **CSS3**, and **JavaScript ES6** to create a dynamic, responsive, and user-friendly web application.

## Features

- Responsive login page with JWT-based authentication
- Dynamic list of places fetched from the API
- Place detail view with real-time data
- Secure form to add a review (authenticated users only)
- Session management using browser cookies
- Seamless client-server interaction using Fetch API
- Client-side country filtering

## Pages

| Page          | Description                                                                                                        |
|---------------|--------------------------------------------------------------------------------------------------------------------|
| `login.html`  | Login form authenticating users via the API and storing the JWT in cookie.                                         |
| `index.html`  | Main page listing all places with a country filter.                                                                |
| `place.html`  | Detailed view of a single place with reviews and review form. Review form accessible only by authenticated users.  |

## Technologies Used

- HTML5, CSS3, JavaScript (ES6)
- Fetch API & AJAX
- JSON Web Tokens (JWT)
- Cookie-based session handling
- Flask API (back-end)

## Usage

1. **Login** via `login.html`
   → A JWT token is stored in a cookie for session management.

2. **Access** the main page `index.html`
   → Fetches a list of places from the back-end.

3. **Click** on a place to view its details in `place.html`
   → Displays full data for the selected place.

4. **Submit** a review (if logged in) using the form in `place.html`
   → Authenticated users can post reviews directly to the API.

## Authentication

- JWT tokens are received from the API during login.
- Tokens are stored in cookies and included in each API request header.
- Unauthenticated users are redirected to the login page.

## Author

This project is part of the **Holberton School Full-Stack Curriculum**.
Developed by Thérèse-Marie Lefoulon.
