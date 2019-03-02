import React, {Component} from 'react';  
import PropTypes from "prop-types";

import CSRFToken from './csrftoken';


class WearingSessionForm extends React.Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired
  };
  
  constructor(props) {
    super(props);
    this.state = {
      wearLocation: '',
      patientID: ''
    };

    this.handleLocationChange = this.handleLocationChange.bind(this);
    this.handlePatientIDChange = this.handlePatientIDChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

    this.endpoint = this.props.endpoint;
    console.log(this.endpoint)
  }

  // handleSubmit(event) {
  //   alert('Mobitrack started: ' + this.state.wearLocation + '    '  + this.state.patientID + '         ' + this.endpoint);
  //   event.preventDefault();
  // }

  handleSubmit(event) {
    // var csrftoken = getCookie('csrftoken');
    // var headers = new Headers();
    // headers.append('X-CSRFToken', csrftoken);
    // headers.append('Content-Type', 'application/json');
    //e.preventDefault();
    const { wearLocation, patientID } = this.state;
    const lead = { wearLocation, patientID };
    const conf = {
      credentials: 'include',
      method: "POST",
      mode: 'same-origin',
      body: JSON.stringify(lead),
      headers: new Headers({ "Content-Type": "application/json" })
    };
    fetch(this.props.endpoint, conf).then(response => console.log("andrea - res" + response)).catch(error => console.log("error====", error));
  };

//   handleSubmit(event) {
//     event.preventDefault();

//     let data = {
//         wearLocation: this.state.wearLocation,
//         patientID: this.state.patientID,
//     };

//     if (this.state.wearLocation !== '' && this.state.patientID !== '' ) {
//         console.log('wearLocation', this.state.wearLocation, 'patientID ', this.state.patientID);

//         fetch("example.com/:id", {
//             method: 'POST',
//             headers: {
//                 'Accept': 'application/json',
//                 'Content-Type': 'application/json',
//             },
//             mode: "cors",
//             body: JSON.stringify(data)
//         })
//             .then(response => response.json())
//             .then(data => console.log(data))
//             .catch(error => console.log(error));

//     } else {
//         alert('no')
//     }
// }

  handleLocationChange(event) {
    this.setState({wearLocation: event.target.value});
  }

  handlePatientIDChange(event) {
    this.setState({patientID: event.target.value});
  }


  render() {
    return (
      <form onSubmit={this.handleSubmit}>
         <label>
          Wearing Location:
          <select value={this.state.wearLocation} onChange={this.handleLocationChange}>
            <option value="left-upper-arm">Left Upper Arm</option>
            <option value="left-lower-arm">Left Lower Arm</option>
            <option value="left-upper-leg">Left Upper Leg</option>
            <option value="left-lower-leg">Left Lower Leg</option>
            <option value="right-upper-arm">Right Upper Arm</option>
            <option value="right-lower-arm">Right Lower Arm</option>
            <option value="right-upper-leg">Right Upper Leg</option>
            <option value="right-lower-leg">Right Lower Leg</option>
          </select>
        </label>

        <br />

        <label>
          Patient ID:
          <input type="text" value={this.state.patientID} onChange={this.handlePatientIDChange} />
        </label>

        <br />
        <input type="submit" value="Start Monitoring" />
      </form>
    );
  }
}
export default WearingSessionForm;