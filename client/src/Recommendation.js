import React from 'react';
import { useLocation } from 'react-router-dom';

function Recommendation() {
  const location = useLocation();
  const recommendations = location.state?.recommendations || [];

    return (
      <div>
        <h2>Recommendations</h2>
        {recommendations && recommendations.length > 0 ? (
          <ul>
            {recommendations.map((movie, index) => (
              <li key={index}>{movie.title}</li>
            ))}
          </ul>
        ) : (
          <p>No recommendations available.</p>
        )}
      </div>
    );
  }
  

export default Recommendation;
