import React, {useState, useEffect}  from 'react';
import './App.css';
// import Header from './components/ui/Header';
// import Datafetch from './components/Cases/Datafetch';
// import Search from './components/ui/Search';
import axios from 'axios';
// import Pagination from './components/ui/Pagination';
import Home from './components/Pages/Home/Home';


const App = () => {
  const[items, setItems] = useState([]);
  const[isLoading, setIsLoading] = useState(true);
  const[query, setQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const[itemsPerPage] = useState(6);

  useEffect(() => {
    const fetchItems = async () => {
      setIsLoading(true)
      // const result = await axios(`http://127.0.0.1:8000/fulltext/cases/${query}`)
      const result = await axios('http://127.0.0.1:8000/cases/')
      // console.log(result.data)
      setItems(result.data)
      // setItems(fullSearchUrl.data)
      setIsLoading(false)
    }
    fetchItems()
  },[query] )

  //Pagination starts here
  //Get current items
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = items.slice(indexOfFirstItem, indexOfLastItem);

  //change page
  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div>
      {/* <Navbar bg="primary" variant="dark">
<div className="container-fluid">
<Navbar.Brand>React-bootstrap</Navbar.Brand>
<Nav className="me-auto">
<Nav.Link href="#home">Home</Nav.Link>
<Nav.Link href="#link">Link</Nav.Link>
</Nav>
</div>
</Navbar> */}
     {/* <Header /> */}
     {/* <Search getQuery={(q) => setQuery(q)} /> */}
     {/* <Datafetch isLoading={isLoading} items={currentItems}/> */}
     {/* <Pagination 
        itemsPerPage={itemsPerPage} 
        totalItems={items.length} 
        paginate={paginate} 
        /> */}
        <Home />
    </div>
  );
}

export default App;
