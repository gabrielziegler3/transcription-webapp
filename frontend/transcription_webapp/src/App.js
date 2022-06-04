import axios from 'axios';

import React, { Component } from 'react';

class App extends Component {
    state = {
        selectedFile: null,
        transcription: null
    };

    onFileChange = (event) => {
        this.setState({ selectedFile: event.target.files[0] });
    };

    onFileUpload = () => {
        const data = new FormData();

        data.append("file", this.state.selectedFile);

        axios
            .post("http://localhost:80/transcript", data)
            .then((response) => {
                this.setState({ transcription: response.data.transcription });
            })
            .catch((error) => {
                console.log(error)
            });
    };

    fileData = () => {
        if (this.state.selectedFile) {
            return (
                <div>
                    <h2>File Details:</h2>
                    <p>File Name: {this.state.selectedFile.name}</p>
                    <p>File Type: {this.state.selectedFile.type}</p>
                    <p>
                        Last Modified:{" "}
                        {this.state.selectedFile.lastModifiedDate.toDateString()}
                    </p>
                </div>
            );
        } else {
            return (
                <div>
                    <br />
                    <h4>Choose before Pressing the Upload button</h4>
                </div>
            );
        }
    };

    transcriptionData = () => {
        if (this.state.transcription) {
            return (
            <div>
                <h2> Transcription: </h2>
                <p> {this.state.transcription} </p>
            </div>
            );
        }
    };

    render() {

        return (
            <div>
                <div>
                    <p align="center">
                        <input type="file" onChange={this.onFileChange} />
                        <button onClick={this.onFileUpload}>
                            Upload
                </button>
                    </p>
                </div>
                {this.fileData()}
                {this.transcriptionData()}
            </div>
        );
    }
}

export default App;