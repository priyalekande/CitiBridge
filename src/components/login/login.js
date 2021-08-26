import React, {Component} from "react";
import loginImg from "../../login.svg";
import axios from 'axios';

export class Login extends Component {
  
  state = {
    response: "",
    username: "",
    password: ""
  }


  loginUser = () => {
    axios.post('http://127.0.0.1:5000/login',{
      username: this.state.username,
      password: this.state.password
    }).then(response => {
        this.setState({
          response: response.data.msg
        })
        if(response.data.msg === "Login succcessful"){
          this.props.history.push('/upload')
        } 
    })
  }

  onChangeUsername = (event) => {
    this.setState({username: event.target.value})
  }

  onChangePassword = (event) => {
    this.setState({password: event.target.value})
  }



  render() {
    console.log(this.props)
    return (
      <div className="base-container" ref={this.props.containerRef}>
        <div className="header">Login</div>
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
              <label htmlFor="password">Password</label>
              <input type="password" name="password" placeholder="password" value={this.state.password} onChange = {(event) => this.onChangePassword(event)}/>
            </div>
          </div>
        </div>
        <div className="footer">
          <button type="button" className="btn" onClick = {this.loginUser}>
            Login
          </button>
          {this.state.response}
        </div>
      </div>
    );
  }
}
