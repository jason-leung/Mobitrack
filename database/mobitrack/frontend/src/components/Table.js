// A stateless component for displaying data within a table in HomePage (OUTDATED)
import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import { MDBDataTable } from 'mdbreact';

const columns = [
	{
		field: "sessionID",
		label: "Session ID",
		sort: "asc"
	},
	{
		field: "PatientID",
		label: "Patient ID",
		sort: "asc"
	},
	{
		field: "location",
		label: "Location",
		sort: "asc"
	},	
	{
		field: "Timestamp",
		label: "Time Recorded",
		sort: "asc"
	}
];

const Table = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="column">
      <MDBDataTable striped bordered hover searching={false} info={false} paging={false} data={{columns:columns, rows:data}}/>
    </div>
  );
Table.propTypes = {
  data: PropTypes.array.isRequired
};
export default Table;