// The Wearing Session component of the React frontend
import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";

const Session = () => (
  <DataProvider endpoint="database/wearingsession/" 
                render={data => <Table data={data} />} />
);

const wrapper = document.getElementById("wearingsession");

wrapper ? ReactDOM.render(<Session />, wrapper) : null;