import React, {Component} from 'react';  
import PropTypes from "prop-types";

const API_URL = 'pairmobitrack'


function updateProgress(task_id, component_ref) {
  console.log('In update progress function: ' + task_id);
  var progressUrl = API_URL+ "/" + task_id;

  fetch(progressUrl).then(function(response) {
    response.json().then(function(data) {
      console.log(data);
      if (data.state == "ANDREA") {
        setTimeout(updateProgress, 500, task_id, component_ref);
      }
      else if (data.state == "PENDING") {
        setTimeout(updateProgress, 500, task_id, component_ref);
      }
      else {
        console.log(component_ref)
        return component_ref.finishedAnswer(data);
      }
    });
  });
}

class WearingSessionForm extends React.Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired
  };
  
  constructor(props) {
    super(props);
    this.state = {
      submitted: false,
      task_id: null,
      wearLocation: 'left-upper-arm',
      patientID: ''
    };


    this.handleLocationChange = this.handleLocationChange.bind(this);
    this.handlePatientIDChange = this.handlePatientIDChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

    this.endpoint = this.props.endpoint;
  }


  setTaskID(id) {
    console.log("got response - setTaskID");  
    this.state.task_id = id['id'];
    console.log(this.state.task_id);
    updateProgress(this.state.task_id, this);
  


  }

  finishedAnswer(result) {
    console.log('DID THIS REALLY JUST WORK???');
    console.log(result)
  }

  handleSubmit(event) {
    event.preventDefault();
    console.log(this.state.submitted + " Sumbitted");

    const { wearLocation, patientID } = this.state;
    const lead = { wearLocation, patientID };
    const conf = {
      credentials: 'include',
      method: "POST",
      mode: 'same-origin',
      body: JSON.stringify(lead),
      headers: new Headers({ "Content-Type": "application/json" })
    };
    console.log("submitted form");

    fetch(this.props.endpoint, conf)
      .then(response => response.json())
      .then(response => this.setTaskID(response))
      .catch(err => console.log(err));
  };

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