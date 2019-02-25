import React, {Component} from 'react';  

class WearingSessionForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      wearLocation: '',
      patientID: ''
    };

    this.handleLocationChange = this.handleLocationChange.bind(this);
    this.handlePatientIDChange = this.handlePatientIDChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    alert('Mobitrack started: ' + this.state.wearLocation + '    '  + this.state.patientID);
    event.preventDefault();
  }

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