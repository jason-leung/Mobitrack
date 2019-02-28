// The Wearing Session component of the React frontend
import React, { Component } from "react";
import PropTypes from "prop-types";

import Table from "./Table";

class Search extends Component {  
  static propTypes = {
	endpoint: PropTypes.string.isRequired,
    render: PropTypes.func.isRequired
  };
  
  constructor(props) {
  	super(props);
  	this.state = {
  		filtered: [],
  		loaded: false,
		placeholder: "Loading..."
  	};
  	this.handleChange = this.handleChange.bind(this);
  }
  
  componentDidMount() {
    fetch(this.props.endpoint)
      .then(response => {
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then(filtered => this.setState({ filtered: filtered, loaded: true }));
  }
  
  handleChange(e) {
  	console.log(e.target.value);
	// Variable to hold the original version of the list
    let currentList = [];
	// Variable to hold the filtered list before putting into state
    let newList = [];
	
	// If the search bar isn't empty
    if (e.target.value !== "") {
      // Assign the original list to currentList
      currentList = this.props.filtered;
            
      // Determine which items should be displayed based on the search terms
      newList = currentList.filter(item => {
        const lc = item.toLowerCase();
        const filter = e.target.value.toLowerCase();
		// Check to see if the current list item includes the search term
        return lc.includes(filter);
      });
    } else {
      // If the search bar is empty, set newList to original task list
      newList = this.props.filtered;
    }
    // Set the filtered state based on what our rules added to newList
    this.setState({filtered: newList});
  }
  
  render() {
    const { filtered, loaded, placeholder } = this.state;
    return loaded ? this.props.render(filtered) : <p>{placeholder}</p>;
  }
}

export default Search;