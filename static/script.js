// const apiKey = '2a4cfcec'; 

// async function searchMovie() {
//   const title = document.getElementById("searchInput").value.trim();
//   const res = await fetch(`https://www.omdbapi.com/?t=${title}&apikey=${apiKey}`);
//   const data = await res.json();
// if (data.Response === "True") {
//   const trailerLink = `https://www.youtube.com/results?search_query=${encodeURIComponent(data.Title + " trailer")}`;

//   document.getElementById("result").innerHTML = `
//     <h2>${data.Title} (${data.Year})</h2>
//     <p><strong>Genre:</strong> ${data.Genre}</p>
//     <p><strong>Actors:</strong> ${data.Actors}</p>
//     <img src="${data.Poster}" width="200"/><br>
//     <a href="${trailerLink}" target="_blank">🎬 Watch Trailer on YouTube</a>
//   `;
//   fetchRecommendations(title);
//   }

//   if (data.Response === "True") {
//     document.getElementById("result").innerHTML = `
//       <h2>${data.Title} (${data.Year})</h2>
//       <p><strong>Genre:</strong> ${data.Genre}</p>
//       <p><strong>Actors:</strong> ${data.Actors}</p>
//       <img src="${data.Poster}" width="200"/>
//     `;
//     fetchRecommendations(title);
//   } else {
//     document.getElementById("result").innerHTML = `<p>Movie not found</p>`;
const apiKey = '2a4cfcec'; 

async function searchMovie() {
  const title = document.getElementById("searchInput").value.trim();
  const res = await fetch(`https://www.omdbapi.com/?t=${title}&apikey=${apiKey}`);
  const data = await res.json();

  if (data.Response === "True") {
    const trailerLink = `https://www.youtube.com/results?search_query=${encodeURIComponent(data.Title + " trailer")}`;

    document.getElementById("result").innerHTML = `
      <h2>${data.Title} (${data.Year})</h2>
      <p><strong>Genre:</strong> ${data.Genre}</p>
      <p><strong>Actors:</strong> ${data.Actors}</p>
      <p><strong>Plot:</strong> ${data.Plot}</p>
      <p><strong>IMDb Rating:</strong> ⭐ ${data.imdbRating}</p>
      <img src="${data.Poster}" width="200"/><br>
      <a href="${trailerLink}" target="_blank">🎬 Watch Trailer on YouTube</a>
    `;
    
    fetchRecommendations(title);
  } else {
    document.getElementById("result").innerHTML = `<p> Movie not found. Try again!</p>`;
  }
}

async function fetchRecommendations(movieTitle) {
  console.log("Fetching recommendations for:", movieTitle); 

  const res = await fetch(`http://127.0.0.1:5000/recommend?movie=${movieTitle}`);
  const recs = await res.json();

  console.log("Received recommendations:", recs); 

  let html = "";
  for (let title of recs) {
    const omdb = await fetch(`https://www.omdbapi.com/?t=${title}&apikey=${apiKey}`);
    const data = await omdb.json();

    if (data.Response === "True") {
      html += `
        <div class="recommend-card">
          <img src="${data.Poster}" alt="${data.Title}" class="poster"/>
          <div class="movie-details">
            <h3>${data.Title} (${data.Year})</h3>
            <p><strong>Genre:</strong> ${data.Genre}</p>
            <p><strong>Actors:</strong> ${data.Actors}</p>
            <p><strong>IMDb Rating:</strong> ⭐ ${data.imdbRating}</p>
            <p><strong>Plot:</strong> ${data.Plot}</p>
          </div>
        </div>
      `;
    }
  }
  document.getElementById("recommendGrid").innerHTML = html;
}
