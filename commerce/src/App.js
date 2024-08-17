import { BrowserRouter, Routes, Route, Link } from "react-router-dom"
import Home from "./components/Home";

// pages

function App() {
  return (
    <BrowserRouter>
      <nav>
        <h1>Products</h1>
        <Link to="/">Home</Link>
        {/* <Link to="/create">Create New Smoothie</Link> */}
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        {/* <Route path="/create" element={<Create />} />
        <Route path="/:id" element={<Update />} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;