import React, {Component} from 'react';  
import PropTypes from "prop-types";

const API_URL = 'pairmobitrack'


function updateProgress(task_id, component_ref) {
  console.log('In update progress function: ' + task_id);
  var progressUrl = API_URL+ "/" + task_id;

  fetch(progressUrl).then(function(response) {
    response.json().then(function(data) {
      if (data.state == "SUCCESS") {
        component_ref.setConnectionStatus(data.state);
        return component_ref.finishedAnswer(data);
      }
      else{
        component_ref.setConnectionStatus(data.state);
        setTimeout(updateProgress, 500, task_id, component_ref);
      }
    });
  });
}

function ConnectionStatus(props) {
  if (!props.status) {
    return null;
  }
  
  return (
    <div>
      Current Mobitrack Status: {props.status}
    </div>
  );
}

function StartButton(props) {
var class_ref = props.obj;
  if(props.visibility){
    return(
      <button className="start btn" onClick={class_ref.handleStartMonitoring} > Start Monitoring</button>
    ) 
  }
  return (
    <button disabled={!props.visibility} className="start btn disabled" onClick={class_ref.handleStartMonitoring} > Start Monitoring</button>
  )
}

function StopButton(props) {
  console.log(props)
  var class_ref = props.obj;
  if(props.visibility){
    return(
      <button className="stop btn" onClick={class_ref.handleStopMonitoring} > Stop Monitoring</button>
    ) 
  }
  return (
    <button disabled={!props.visibility} className="stop btn disabled" onClick={class_ref.handleStopMonitoring} > Stop Monitoring</button>
    )
}

class WearingSessionForm extends React.Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired
  };
  
  constructor(props) {
    super(props);
    this.state = {
      startedMonitoring: false,
      startMonitoringButtonActive: true,
      task_id: null,
      wearLocation: 'left-upper-arm',
      patientID: '',
      connectionStatus: null,
      led_on: false,
      target_angle: 45,
    };


    this.handleLocationChange = this.handleLocationChange.bind(this);
    this.handlePatientIDChange = this.handlePatientIDChange.bind(this);
    this.handleStartMonitoring = this.handleStartMonitoring.bind(this);
    this.handleStopMonitoring = this.handleStopMonitoring.bind(this);
    this.setConnectionStatus = this.setConnectionStatus.bind(this);
    this.handleCheckBox = this.handleCheckBox.bind(this);

    this.endpoint = this.props.endpoint;
  }

  componentWillMount() {

    const { wearLocation, patientID } = this.state;
    const lead = { wearLocation, patientID };
    const conf = {
      credentials: 'include',
      method: "POST",
      mode: 'same-origin',
      body: JSON.stringify(lead),
      headers: new Headers({ "Content-Type": "application/json" })
    };

    var fetchURL = this.props.endpoint + "getStatus/";
    fetch(fetchURL, conf)
      .then(response => response.json())
      .then(response => this.checkIfAlreadyRunning(response))
      .catch(err => console.log(err));

  }

  checkIfAlreadyRunning(response) {
    if(response['currently_running']) {
      this.setState({startMonitoringButtonActive: false});
      this.setTaskID(response)
    } 
    console.log("currently not monitoring");
  }

  setTaskID(id) {
    this.state.task_id = id['task_id'];
    console.log(this.state.task_id);
    updateProgress(this.state.task_id, this);
  }

  setConnectionStatus(status) {
    this.setState({connectionStatus: status});
  }

  finishedAnswer(result) {
    // Reset to original view
    this.setState({startMonitoringButtonActive: true, connectionStatus: null});
    console.log(result)
  }

  handleStartMonitoring(event) {
    event.preventDefault();
    console.log(this.state.startedMonitoring + " Sumbitted");
    this.setState({startMonitoringButtonActive: false});


    const { wearLocation, patientID, led_on, target_angle } = this.state;
    const lead = { wearLocation, patientID, led_on, target_angle};
    const conf = {
      credentials: 'include',
      method: "POST",
      mode: 'same-origin',
      body: JSON.stringify(lead),
      headers: new Headers({ "Content-Type": "application/json" })
    };
    console.log("submitted form");


    var fetchURL = this.props.endpoint + "submit/";
    fetch(fetchURL, conf)
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

  handleCheckBox(event) {
    this.setState({led_on: !this.state.checked});
  }

  handleTargetAngleChange(event) {
    this.setState({target_angle: event.target.value});
  }

  handleStopMonitoring(event){
    event.preventDefault();
    this.setState({startMonitoringButtonActive: true});
    const { wearLocation, patientID } = this.state;
    const lead = { wearLocation, patientID };
    const conf = {
      credentials: 'include',
      method: "POST",
      mode: 'same-origin',
      body: JSON.stringify(lead),
      headers: new Headers({ "Content-Type": "application/json" })
    };

    var fetchURL = this.props.endpoint + "stopMonitoring/";
    fetch(fetchURL, conf)
      .then(response => response.json())
      .catch(err => console.log(err));
  }


  render() {
    return (
      <div> 

      <form >
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

        <label>
          Target ROM:  
          <input type="text" value={this.state.target_angle} onChange={this.handleTargetAngleChange} />
        </label>


        <br />
        LED on:  
        <input type="checkbox" onChange={this.handleCheckBox} defaultChecked={this.state.led_on} />

        <br />
        <StartButton visibility={this.state.startMonitoringButtonActive} obj={this}/>
        <StopButton visibility={!this.state.startMonitoringButtonActive} obj={this} />
      </form>
        <ConnectionStatus status={this.state.connectionStatus} />
      </div>
    );
  }
}
export default WearingSessionForm;