import React from "react";
import "./App.css";
import { Typography } from "@material-ui/core";

import UploadFiles from "./components/upload-files.component";

function Transcript() {
  return (
    <div className="container">
      <div className="mg20">
        <Typography variant="h5">Audio transcription</Typography>
      </div>
      <UploadFiles />
    </div>
  );
}

export default Transcript;