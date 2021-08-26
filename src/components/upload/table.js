import React, {Component} from 'react';
import axios from 'axios';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import {Link} from "react-router-dom";

const URL_FIELDS = 'http://localhost:3004/fields'
var num = 0;
class TableComp extends Component{

    state = {
        fields: [],
        file: null
    }

    componentDidMount(){
        // axios.get(URL_FIELDS)
        // .then( response => {
        //     this.setState({fields: response.data })
        // })
    }

    handleUploadImage(ev) {
        alert("Your file is being uploaded!");
    }


    logoutUser = () => {
        window.location.href = 'http://localhost:3000';
        

      }


    fileUpload = (event) => {

        let file = event.target.files[0]
        let formdata = new FormData()
        
        formdata.append("csv_file", file)
        formdata.append("name", "Citi")

        const config = {     
            headers: { 'content-type': 'multipart/form-data' }
        }

        axios.post('http://127.0.0.1:5000/upload', formdata, config)
            .then(response => {
                this.setState({fields: response.data.records})
                console.log(response.data.records)
            })

        alert("Feed generated successfully");
        
    }



   
    render(){

        return (
            <div className = "transactions">

        
                <div className="header">
                    <label>Clearing Feed Generator</label>
                    </div>           
                <input
                    accept=".csv"
                    className="upload"
                    id="contained-button-file"
                    
                    type="file"
                    onChange = {(event) => this.fileUpload(event)}
                />

                <label htmlFor="contained-button-file">
                    <div className="buttons">
                    <Button variant="contained" color="primary" component="span" >
                        Upload
                    </Button>
                    </div>
                </label>

                <div className="buttons">
                    <Button variant="contained" color="primary" component="span" onClick = { this.logoutUser} >
                        Log Out
                    </Button>
                </div>


                

                {/* <label className = "label">Clearing Feed</label>  */}
            
                {console.log("rendered")}
                <TableContainer component={Paper} className = "table-container">
                    <Table aria-label="simple table" className = "table">
                    <TableHead>
                        <TableRow>
                        <TableCell>Transaction_ref_no</TableCell>
                        <TableCell align="right">Value Date</TableCell>
                        <TableCell align="right">Payer</TableCell>
                        <TableCell align="right">Payer Account</TableCell>
                        <TableCell align="right">Payee</TableCell>
                        <TableCell align="right">Payee Account</TableCell>
                        <TableCell align="right">Amount</TableCell>
                        <TableCell align="right">Status</TableCell>
                        </TableRow>
                    </TableHead>
                    
                    <TableBody>
                        {console.log(this.state.fields)}
                        {this.state.fields ? 
                        this.state.fields.map((row) => (
                        
                        <TableRow key = {row.transaction_ref_no}>
                            <TableCell component="th" scope="row">
                            {row.transactionref}
                            </TableCell>
                            <TableCell align="right">{row.Date}</TableCell>
                            <TableCell align="right">{row.payer}</TableCell>
                            <TableCell align="right">{row.payeracc}</TableCell>
                            <TableCell align="right">{row.payee}</TableCell>
                            <TableCell align="right">{row.payeeacc}</TableCell>
                            <TableCell align="right">{row.Amount}</TableCell>
                            <TableCell align="right">{row.validate}</TableCell>
                        </TableRow>

                        )): null }
                    </TableBody>
                    </Table>
                </TableContainer>
                
                


              </div>

              
              
        );
    }
    
  }
  export default TableComp;
  