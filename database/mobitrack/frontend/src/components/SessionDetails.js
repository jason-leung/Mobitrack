// The Wearing Session component of the React frontend
import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";

const SessionDetails = () => (
  <DataProvider endpoint="database/exerciseperiod/<sessionID>" 
                render={data => <Table data={data} />} />
);

const wrapper = document.getElementById("sessiondetails");
const sessionID = data.sessionID

wrapper ? ReactDOM.render(<SessionDetails />, wrapper, sessionID) : null;