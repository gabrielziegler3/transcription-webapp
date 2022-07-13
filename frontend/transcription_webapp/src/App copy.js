import axios from 'axios';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
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
                console.log(response)
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
        const card = (
            <React.Fragment>
                <CardContent>
                    <Typography variant="h5" component="div">
                        Transcription
              </Typography>
                    <Typography variant="body2">
                        {this.state.transcription}
                    </Typography>
                </CardContent>
            </React.Fragment>
        );

        if (this.state.transcription) {
            return (
                <Box sx={{ minWidth: 275, maxWidth: 600, align: "center" }}>
                    <Card variant="outlined" align="center">{card}</Card>
                </Box>
            );
        }
    };

    optionsGrid = () => {
        return (
            // <Box sx={{ flexGrow: 1 }}>
                <Grid container spacing={2}>
                    <Grid item xs={8}>
                            <Button variant="contained" component="label">
                                Select File
                            <input type="file" hidden onChange={this.onFileChange} />
                            </Button>
                    </Grid>
                    <Grid item xs={4}>
                            <Button variant="contained" onClick={this.onFileUpload}>Upload</Button>
                    </Grid>
                </Grid>
            // </Box>
        );
    };

    render() {
        return (
            <div>
                {this.optionsGrid()}
            </div>
        )
        // return (
        //     <div>
        //         <div>
        //             <Box sx={{ minWidth: 275 }}>
        //                 <Stack spacing={2} direction="row" align="center">
        //                     <Button variant="contained" component="label" color="primary">
        //                         Select File
        //                     <input type="file" hidden onChange={this.onFileChange} />
        //                     </Button>
        //                     <Button variant="contained" onClick={this.onFileUpload}>Upload</Button>
        //                 </Stack>
        //             </Box>
        //         </div>
        //         {this.fileData()}
        //         {this.transcriptionData()}
        //     </div>
        // );
    }
}

export default App;