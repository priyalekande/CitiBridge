import React, { Component } from 'react'
import DragAndDrop from './dragdrop'
import Button from '@material-ui/core/Button';
class FileList extends Component {
state = {
    files: [
      'nice.pdf',
      'verycool.jpg',
      'amazing.png',
      'goodstuff.mp3',
      'thankyou.doc'
    ]
  }
 handleDrop = (files) => {
    let fileList = this.state.files
    for (var i = 0; i < files.length; i++) { 
      if (!files[i].name) return
      fileList.push(files[i].name)
    }
    this.setState({files: fileList})
  }
render() {
    return (
        <>
        {/* <input
            accept=".csv"
            className="upload"
            id="contained-button-file"
            multiple
            type="file"
        />
        <label htmlFor="contained-button-file">
            <Button variant="contained" color="primary" component="span">
                Upload
            </Button>
        </label> */}
        
        <DragAndDrop handleDrop={this.handleDrop}>
            <div style={{height: 300, width: 250}}>
            {this.state.files.map((file) =>
                <div >{file}</div>
            )}
            </div>
        </DragAndDrop>
      </>
    )
  }
}
export default FileList