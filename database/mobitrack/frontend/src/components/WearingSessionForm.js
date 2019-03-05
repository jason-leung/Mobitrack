import React, {Component} from 'react';  
import PropTypes from "prop-types";

const API_URL = 'pairmobitrack'


function updateProgress(task_id, component_ref) {
  console.log('In update progress function: ' + task_id);
  var progressUrl = API_URL+ "/" + task_id;
  console.log(progressUrl + "progressURL");

  fetch(progressUrl).then(function(response) {
    response.json().then(function(data) {
      console.log(data);
      if (data.state == "ANDREA") {
        console.log('andrea')
        setTimeout(updateProgress, 500, task_id, component_ref);
      }
      else if (data.state == "PENDING") {
        console.log('pending')
        setTimeout(updateProgress, 500, task_id, component_ref);
      }
      else {
        console.log(component_ref)
        return component_ref.finishedAnswer();
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
    // this.updateProgress = this.updateProgress.bind(this);

    this.endpoint = this.props.endpoint;
  }


  setTaskID(id) {
    console.log("got response - setTaskID");  
    this.state.task_id = id['id'];
    console.log(this.state.task_id);
    updateProgress(this.state.task_id, this);
  


  }

  finishedAnswer() {
    console.log('DID THIS REALLY JUST WORK???');
  }

  // updateProgress(task_id) {
  //     console.log('In update progress function: ' + task_id);
  //     var progressUrl = API_URL+ "/" + task_id;
  //     console.log(progressUrl + "progressURL");
    
  //     fetch(progressUrl).then(function(response) {
  //       response.json().then(function(data) {
  //         console.log(data);
  //         if (data.state == "ANDREA") {
  //           console.log('andrea')

  //           setTimeout(
  //             function() {
  //                 this.updateProgress(task_id);
  //             }
  //             .bind(this),
  //             500
  //         );

  //         }
  //         else if (data.state == "PENDING") {
  //           console.log('pending')
  //           setTimeout(
  //             function() {
  //                 this.updateProgress(task_id);
  //             }
  //             .bind(this),
  //             500
  //         );          }
  //         else {
  //           return 227;
  //         }
  //       });
  //     });
  //   }

  //  updateProgress(task_id) {
  //   console.log('In update progress function: ' + task_id);
  //   var progressUrl = API_URL+ "/" + task_id;
  //   console.log(progressUrl + "progressURL");
  
  //   fetch(progressUrl).then(function(response) {
  //     response.json().then(function(data) {
  //       console.log(data);
  //       if (data.state == "ANDREA") {
  //         console.log('andrea')

  //         setTimeout(this.updateProgress.bind(this, task_id, 500));
  //       }
  //       else if (data.state == "PENDING") {
  //         console.log('pending')
  //         setTimeout(this.updateProgress.bind(this, task_id, 500));

  //       }
  //       else {
  //         return 227;
  //       }
  //     });
  //   });
  // }




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

    // fetch(this.props.endpoint, conf)
    //   .then(response => this.setTaskID(
    //         response.json()))
    //   .catch(err => console.log(err));

    fetch(this.props.endpoint, conf)
      .then(response => response.json())
      .then(response => this.setTaskID(response))
      .catch(err => console.log(err));

      


    // fetch(this.props.endpoint, conf).then(function(response){
    //   response.json().then(function(data)
    //   {
    //     this.setTaskID(data);



    //     console.log("got response");  

    //   });
      


    // });


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