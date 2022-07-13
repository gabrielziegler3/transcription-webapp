import React from "react";
import "./App.css";
// import { Typography } from "@material-ui/core";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import UploadFiles from "./components/upload-files.component";
import Home from "./components/home.component";
import Transcript from "./Transcript"
import Sidebar from "./components/sidebar.component"

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Transcript />}>
                    <Route index element={<Home />} />
                    <Route path="transcript" element={<Transcript />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}
//   return (
//     <div className="container">
//       <div className="mg20">
//         <Typography variant="h5">Audio transcription</Typography>
//       </div>
//       <UploadFiles />
//     </div>
//   );
// }

export default App;