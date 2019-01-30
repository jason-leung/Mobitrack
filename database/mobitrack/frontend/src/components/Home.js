// The Home component of the React frontend
import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";

const Home = () => (
  <DataProvider endpoint="latestsession/" 
                render={data => <Table data={data} />} />
);

const wrapper = document.getElementById("home");

wrapper ? ReactDOM.render(<Home />, wrapper) : null;