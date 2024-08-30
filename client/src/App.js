import React, { useState, useEffect } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import Recommendation from './Recommendation';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [reviewer, setReviewer] = useState('');
  const [genre, setGenre] = useState('');
  const [reviewers, setReviewers] = useState([]);
  const [genres, setGenres] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://127.0.0.1:5000/show_reviewer')
      .then((response) => response.json())
      .then((data) => setReviewers(data))
      .catch((error) => console.error('Error fetching reviewers:', error));
  }, []);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/genres')
      .then((response) => response.json())
      .then((data) => setGenres(data))
      .catch((error) => console.error('Error fetching genres:', error));
  }, []);

  const getRecommendation = () => {
    fetch('http://127.0.0.1:5000/recommendations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ movie_name: searchTerm }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (!data.error) {
          navigate('/recommendations', { state: { recommendations: data } });
        } else {
          console.error(data.error);
        }
      })
      .catch((error) => console.error('Error fetching recommendations:', error));
  };

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleReviewerChange = (event) => {
    setReviewer(event.target.value);
  };

  const handleGenreChange = (event) => {
    setGenre(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    getRecommendation();
  };

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Welcome to Movie Recommendation</h1>
          <p>Find your next favorite movie!</p>
          <form onSubmit={handleSearchSubmit}>
            <input
              type="text"
              placeholder="Search for a movie..."
              value={searchTerm}
              onChange={handleSearchChange}
              className="search-bar"
            />
            <select value={reviewer} onChange={handleReviewerChange} className="dropdown">
              <option value="">Select Reviewer</option>
              {reviewers.map((rev, index) => (
                <option key={index} value={`${rev["First name "]} ${rev["Last name"]}`}>
                  {`${rev["First name "]} ${rev["Last name"]}`}
                </option>
              ))}
            </select>
            <select value={genre} onChange={handleGenreChange} className="dropdown">
              <option value="">Select Genre</option>
              {genres.map((genre, index) => (
                <option key={index} value={genre}>{genre}</option>
              ))}
            </select>
            <button type="submit" className="search-button">Search</button>
          </form>
        </header>
        <Routes>
          <Route path="/recommendations" element={<Recommendation />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
