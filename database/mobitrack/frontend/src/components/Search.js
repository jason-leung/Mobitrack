// The Wearing Session component of the React frontend
import React, { Component } from "react";
import PropTypes from "prop-types";

const API_URL = 'database/exerciseperiod';

class Search extends Component {  
  static propTypes = {
    render: PropTypes.func.isRequired
  };

  constructor(props) {
  	super(props);
  	this.state = {
  		error: false,
  		query: null,
  		results: [],
  	};
  	this.searchByID();
  	this.handleChange = this.handleChange.bind(this);
  }
  
  searchByID = () => {
	fetch(API_URL+ "/" + this.state.query)
	  .then(response => {
	  	return response.json();
	  })
	    .then(results => this.setState({
	  	  results: results
	    }))
  }
  
  handleChange(e) {
	this.setState({
	  query: e.target.value
	}, () => {
		console.log("The query string is");
		console.log(this.state.query);
		this.searchByID();
	})
  }
  
  handleSubmit(e) {
  	e.preventDefault();
  }

  render() {
    const { query, results } = this.state;
    return ([
		<form className="form-inline active-purple-4" onKeyPress={this.handleEnter} onSubmit={this.handleSubmit}>
		  <input className="form-control form-control-sm mr-3 w-75" placeholder="Search by PatientID" ref={input => this.search = input} onChange={this.handleChange} onSubmit={this.handleSubmit}/>
		</form>,
		this.props.render(this.state.results)
	])
  } 
}

export default Search;