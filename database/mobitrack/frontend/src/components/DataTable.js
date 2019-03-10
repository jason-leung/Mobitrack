// A stateless component for displaying data within a table for all wearing session
import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import { MDBDataTable } from 'mdbreact';

const columns = [
	{
		field: "PeriodID",
		label: "Period ID",
		sort: "asc"
	},
	{
		field: "PatientID",
		label: "Patient ID",
		sort: "asc"
	},
	{
		field: "Duration",
		label: "Duration",
		sort: "asc"
	},
	{
		field: "Repetitions",
		label: "Repetitions",
		sort: "asc"
	},	
	{
		field: "Timestamp",
		label: "Time Recorded",
		sort: "asc"
	},
	{
		field: "SessionID",
		label: "Session ID",
		sort: "asc"
	}
];
		
const DataTable = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="column">
      <MDBDataTable striped bordered hover searching={false} data={{columns:columns, rows:data}}/>
    </div>
  );
DataTable.propTypes = {
  data: PropTypes.array.isRequired
};
export default DataTable;