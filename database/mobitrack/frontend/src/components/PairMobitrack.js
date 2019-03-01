// The Wearing Session component of the React frontend
import React from "react";
import ReactDOM from "react-dom";
import WearingSessionForm from "./WearingSessionForm";

const Form = () => (
  <WearingSessionForm endpoint = "pairmobitrack/submit/"
  />
);

const wrapper = document.getElementById("pairmobitrack");

wrapper ? ReactDOM.render(<Form />, wrapper) : null;