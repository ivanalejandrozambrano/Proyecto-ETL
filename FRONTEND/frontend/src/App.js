import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { About } from "./components/About";
import { Data } from "./components/Data";
const styles = {
  body: {
    margin: 0,
    padding: 0,
    background: "url('https://cdn.pixabay.com/photo/2015/02/25/09/12/brook-648512_1280.jpg') no-repeat center center fixed",
    backgroundSize: "cover",
    fontFamily: "Arial, sans-serif",
    color: "#fff",
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",

  }
};
function App() {
  return (
    <Router>
      <Navbar />

      <div style={styles.body}>
        <Routes>
          <Route path="/about" element={<About />} />
          <Route path="/" element={<Data />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
