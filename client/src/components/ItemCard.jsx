import React from 'react';

const ItemCard = ({ item }) => {

    return (
        <div className="bg-white rounded-lg w-60 h-60 shadow-md p-6 mb-4">
            <img src="https://www.google.com/imgres?q=gold%20chain%20image%20hd&imgurl=https%3A%2F%2Ft4.ftcdn.net%2Fjpg%2F05%2F32%2F82%2F23%2F360_F_532822388_FG1byOJ42sWgG6gMJqW8b7fbron08Czz.jpg&imgrefurl=https%3A%2F%2Fstock.adobe.com%2Fsearch%2Fimages%3Fk%3Dgold%2Bchain&docid=pkb3CG11JpMbqM&tbnid=f6tzYpO90VVPIM&vet=12ahUKEwjMgOuJ7JGGAxWkwzgGHdKXC54QM3oECH8QAA..i&w=581&h=360&hcb=2&ved=2ahUKEwjMgOuJ7JGGAxWkwzgGHdKXC54QM3oECH8QAA" alt="Not showing" />
            <h2 className="text-lg font-bold mb-2">{item.name}</h2>
            <p className="text-gray-700 mb-2">Price: ${item.price}</p>
            <p className="text-gray-700 mb-4">{item.description}</p>
        </div>
    );
};

export default ItemCard;
