// A stateless component for displaying data within a table for all wearing session
import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import { MDBDataTable } from 'mdbreact';

const columns = [
	{
		field: "PeriodID",
		label: "Period ID",
		sortable: false
	},
	{
		field: "PatientID",
		label: "Patient ID",
		sort: "asc"
	},
	{
		field: "TargetROM",
		label: "Target ROM",
		sortable: false
	},
	{
		field: "Duration",
		label: "Duration",
		sortable: false
	},
	{
		field: "Repetitions",
		label: "Repetitions",
		sortable: false
	},
	{
		field: "Timestamp",
		label: "Time Recorded",
		sort: "asc",
	},
	{
		field: "SessionID",
		label: "Session ID",
		sortable: false
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