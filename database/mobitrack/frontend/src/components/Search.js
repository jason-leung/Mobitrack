import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";

class SearchBar extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      search : '',
      url : '',
      redirect : false
    }

    this.handleChange = this.handleChange.bind(this);
    this.handleSearch = this.handleSearch.bind(this);
  }
  // Modify the search key of the component state
  handleChange (e) {
    this.setState({
      search : e.target.value
    });
  }
  // gets the user input
  // and build the url based on it
  handleSearch (e) {
    e.preventDefault(); // prevent page reload
    const { search } = this.state;
    const url = `your_url/search/?q=${encodeURIComponent(search)}`;

	const SessionDetails = () => (
	  <DataProvider endpoint="database/exerciseperiod/<search>" 
					render={data => <Table data={data} />} />
	);

	const wrapper = document.getElementById("sessiondetails");
	const sessionID = data.sessionID;
    console.log(url)

    // re-render the component
    this.setState({
      url,
      redirect : true
    });
    // that will force your component to rerender
  }

  render () {
    const { search, url, redirect } = this.state;
    // if you are using react-router-dom just 
    // render a Redirect Component
    if (redirect) {
       return <Redirect to={url} />
    }
    //
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