import React, { useState } from "react";
import axios from "axios";

function HousePriceApp() {
  const [form, setForm] = useState({
    Total_Area: "",
    Price_per_SQFT: "",
    Baths: "",
    Balcony: "",
    City: "",
    BHK: ""
  });
  const [price, setPrice] = useState(null);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/predict`, form);
        setPrice(response.data.predicted_price);
    } catch (error) {
      console.error("Error fetching prediction:", error);
    }
  };

  return (
    <div>
      <h1>HomeScope</h1>
      <h2>🏠 House Price Predictor</h2>
      <form onSubmit={handleSubmit} class="master-form">
        <div className="form">
            <div className="form-col">
                <label>Total Area (sqft) : </label>
                <input name="Total_Area" onChange={handleChange} placeholder="Total Area (sqft)" class="inputs" />
                <label>Price per sqft : </label>
                <input name="Price_per_SQFT" onChange={handleChange} placeholder="Price per Sqft" class="inputs"/>
                <label>Baths : </label>
                <input name="Baths" onChange={handleChange} placeholder="Bathrooms" class="inputs"/>
            </div>
            <div className="form-col">
                <label>Balcony : </label>
                <input name="Balcony" onChange={handleChange} placeholder="Balcony (1 or 0)" class="inputs"/>
                <label>City : </label>
                <input name="City" onChange={handleChange} placeholder="City (e.g. Pune, Mumbai)" class="inputs"/>
                <label>BHK : </label>
                <input name="BHK" onChange={handleChange} placeholder="BHK" class="inputs"/>
            </div>
        </div>
        <button type="submit">Predict</button>
      </form>
      {price && <h3>Predicted Price: {price}</h3>}

    </div>
  );
}

export default HousePriceApp;