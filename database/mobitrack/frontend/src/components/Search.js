import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";

class Search extends React.Component {
  constructor(props) {
  	super(props);
  	this.state = {
  		search: '',
  		url: '',
  	}
  }
  
  handleChange(e) {
  	current_data = null;
  	if (e.target.value !== "") {
  		current_data = this.props.items;
  	}
  	
  	const SessionDetail = () => (
  		<DataProvider endpoint="database/exerciseperiod/<sessionID>" 
                render={data => <Table data={data} />} />
  	);
  	const wrapper = document.getElementById("sessiondetails");
	const sessionID = current_data.search;
  }
  	
  render() {
  	const { search, url } = this.state;
  	return (
      <form onSubmit={this.handleSearch}>
        <input 
          value={search}
          onChange={this.handleChange}/>
        <button type="submit">Search</button>
      </form>
    );
  }
}