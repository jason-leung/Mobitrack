// The Wearing Session component of the React frontend
import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";
import Search from "./Search";

const Session = () => (
  <Search endpoint="database/exerciseperiod/"
          render={filtered => <Table data={filtered} />} />
);

const wrapper = document.getElementById("wearingsession");

wrapper ? ReactDOM.render(<Session />, wrapper) : null;