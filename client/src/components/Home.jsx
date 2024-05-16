import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="container mx-auto mt-10">
      <h1 className="text-3xl mb-4">Welcome to Our Online Store!</h1>
      <p className="mb-4">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam efficitur, lorem vel maximus efficitur, velit lacus eleifend risus, vel lacinia nulla dui in sem. Curabitur tempus vehicula lorem ac tristique.</p>
      <Link to="/login" className="text-indigo-500">Login</Link> or <Link to="/signup" className="text-indigo-500">Signup</Link>
    </div>
  );
};

export default Home;
