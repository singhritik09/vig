import React from 'react';

const ItemCard = ({ item }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4">
      <h2 className="text-xl font-bold mb-2">{item.name}</h2>
      <p className="text-gray-700 mb-2">Price: ${item.price}</p>
      <p className="text-gray-700 mb-4">{item.description}</p>
    </div>
  );
};

export default ItemCard;
