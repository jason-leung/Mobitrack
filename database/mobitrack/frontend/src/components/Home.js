// The Home component of the React frontend
import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";
import Sidebar from "./Sidebar";

const Home = () => (
  <DataProvider endpoint="database/latestsession/" 
                render={data => <Table data={data} />} />
);

const wrapper = document.getElementById("home");

wrapper ? ReactDOM.render(<Home />, wrapper) : null;