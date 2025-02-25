import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";
import { Box, CardMedia } from "@mui/material";
import React from "react";
import { ThreejsArtifactViewer, isThreejsArtifact, } from "./ThreejsArtifactViewer";
import { WaveSurferArtifactViewer } from "./WaveSurferArtifactViewer";
export const ArtifactCardMedia = ({ artifact, urlPath, height }) => {
    if (isThreejsArtifact(artifact)) {
        return (React.createElement(ThreejsArtifactViewer, { src: urlPath, width: "100%", height: height, hasGizmo: false, filetype: artifact.filename.split(".").pop() }));
    }
    else if (artifact.mimetype.startsWith("video")) {
        return (React.createElement("video", { controls: true, style: {
                width: "100%",
                height: "auto",
            } },
            React.createElement("source", { src: urlPath, type: artifact.mimetype })));
    }
    else if (artifact.mimetype.startsWith("audio")) {
        return (React.createElement(Box, { component: "div", style: {
                width: "100%",
                height: height,
                display: "flex",
                alignItems: "center",
            } },
            React.createElement(WaveSurferArtifactViewer, { height: 100, waveColor: "rgb(200, 0, 200)", progressColor: "rgb(100, 0, 100)", url: urlPath })));
    }
    else if (artifact.mimetype.startsWith("image")) {
        return (React.createElement(CardMedia, { component: "img", height: height, image: urlPath, alt: artifact.filename, style: {
                objectFit: "contain",
            } }));
    }
    return React.createElement(InsertDriveFileIcon, { sx: { fontSize: 80, flexGrow: 1 } });
};
//# sourceMappingURL=ArtifactCardMedia.js.map