// The Wearing Session component of the React frontend
import React from "react";
import ReactDOM from "react-dom";
import Table from "./Table";
import Search from "./Search";

const Session = () => (
  <Search render={results => <Table data={results} />} />
);

const wrapper = document.getElementById("wearingsession");

wrapper ? ReactDOM.render(<Session />, wrapper) : null;