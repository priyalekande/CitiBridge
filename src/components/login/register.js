import React from "react";
import loginImg from "../../login.svg";
import axios from 'axios';

export class Register extends React.Component {
  
  state = {
    response: "",
    username: "",
    password: "",
    email: ""
  }

  registerUser = () => {
    axios.post('http://127.0.0.1:5000/register',{
      username: this.state.username,
      password: this.state.password,
      email: this.state.email
    }).then(response => {
        this.setState({response: response.data.msg}) 
        if(response.data.msg === "You have successfully registered !"){
          this.props.history.push('/upload')
        }
    })
  }

  onChangeUsername = (event) => {
    this.setState({username: event.target.value})
  }

  onChangeEmail = (event) => {
    this.setState({email: event.target.value})
  }

  onChangePassword = (event) => {
    this.setState({password: event.target.value})
  }

  render() {
    return (
      <div className="base-container" ref={this.props.containerRef}>
        <div className="header">Register</div>
        <div className="content">
          <div className="image">
            <img src={loginImg} />
          </div>
          <div className="form">
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input type="text" name="username" placeholder="username" value={this.state.username} onChange = {(event) => this.onChangeUsername(event)}/>
            </div>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input type="text" name="email" placeholder="email" value={this.state.email} onChange = {(event) => this.onChangeEmail(event)}/>
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input type="text" name="password" placeholder="password" value={this.state.password} onChange = {(event) => this.onChangePassword(event)}/>
            </div>
          </div>
        </div>
        <div className="footer">
          <button type="button" className="btn" onClick = {this.registerUser}>
            Register
          </button>
          {this.state.response}
        </div>
      </div>
    );
  }
}