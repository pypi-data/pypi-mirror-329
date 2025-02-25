import DeleteIcon from "@mui/icons-material/Delete";
import DownloadIcon from "@mui/icons-material/Download";
import FullscreenIcon from "@mui/icons-material/Fullscreen";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import { Box, Card, CardActionArea, CardContent, IconButton, Typography, useTheme, } from "@mui/material";
import React, { useRef, useState, } from "react";
import { actionCreator } from "../../action";
import { useArtifactBaseUrlPath } from "../../hooks/useArtifactBaseUrlPath";
import { ArtifactCardMedia } from "./ArtifactCardMedia";
import { useDeleteStudyArtifactDialog } from "./DeleteArtifactDialog";
import { isTableArtifact, useTableArtifactModal } from "./TableArtifactViewer";
import { isThreejsArtifact, useThreejsArtifactModal, } from "./ThreejsArtifactViewer";
const getStudyArtifactUrlPath = (baseUrlPath, studyId, artifactId) => {
    return `${baseUrlPath}/artifacts/${studyId}/${artifactId}`;
};
export const StudyArtifactCards = ({ study }) => {
    const theme = useTheme();
    const artifactBaseUrl = useArtifactBaseUrlPath();
    const [openDeleteArtifactDialog, renderDeleteArtifactDialog] = useDeleteStudyArtifactDialog();
    const [openThreejsArtifactModal, renderThreejsArtifactModal] = useThreejsArtifactModal();
    const [openTableArtifactModal, renderTableArtifactModal] = useTableArtifactModal();
    const width = "200px";
    const height = "150px";
    const artifacts = [...study.artifacts].sort((a, b) => {
        if (a.filename < b.filename) {
            return -1;
        }
        else if (a.filename > b.filename) {
            return 1;
        }
        else {
            return 0;
        }
    });
    return (React.createElement(React.Fragment, null,
        React.createElement(Box, { component: "div", sx: { display: "flex", flexWrap: "wrap", p: theme.spacing(1, 0) } },
            artifacts.map((artifact) => {
                const urlPath = getStudyArtifactUrlPath(artifactBaseUrl, study.id, artifact.artifact_id);
                return (React.createElement(Card, { key: artifact.artifact_id, sx: {
                        marginBottom: theme.spacing(2),
                        width: width,
                        margin: theme.spacing(0, 1, 1, 0),
                        border: `1px solid ${theme.palette.divider}`,
                    } },
                    React.createElement(ArtifactCardMedia, { artifact: artifact, urlPath: urlPath, height: height }),
                    React.createElement(CardContent, { sx: {
                            display: "flex",
                            flexDirection: "row",
                            padding: `${theme.spacing(1)} !important`,
                        } },
                        React.createElement(Typography, { sx: {
                                p: theme.spacing(0.5, 0),
                                flexGrow: 1,
                                wordWrap: "break-word",
                                maxWidth: `calc(100% - ${isThreejsArtifact(artifact)
                                    ? theme.spacing(12)
                                    : theme.spacing(8)})`,
                            } }, artifact.filename),
                        isThreejsArtifact(artifact) ? (React.createElement(IconButton, { "aria-label": "show artifact 3d model", size: "small", color: "inherit", sx: { margin: "auto 0" }, onClick: () => {
                                openThreejsArtifactModal(urlPath, artifact);
                            } },
                            React.createElement(FullscreenIcon, null))) : null,
                        isTableArtifact(artifact) ? (React.createElement(IconButton, { "aria-label": "show artifact table", size: "small", color: "inherit", sx: { margin: "auto 0" }, onClick: () => {
                                openTableArtifactModal(urlPath, artifact);
                            } },
                            React.createElement(FullscreenIcon, null))) : null,
                        React.createElement(IconButton, { "aria-label": "delete artifact", size: "small", color: "inherit", sx: { margin: "auto 0" }, onClick: () => {
                                openDeleteArtifactDialog(study.id, artifact);
                            } },
                            React.createElement(DeleteIcon, null)),
                        React.createElement(IconButton, { "aria-label": "download artifact", size: "small", color: "inherit", download: artifact.filename, sx: { margin: "auto 0" }, href: urlPath },
                            React.createElement(DownloadIcon, null)))));
            }),
            React.createElement(StudyArtifactUploader, { study: study, width: width, height: height })),
        renderDeleteArtifactDialog(),
        renderThreejsArtifactModal(),
        renderTableArtifactModal()));
};
const StudyArtifactUploader = ({ study, width, height }) => {
    const theme = useTheme();
    const [dragOver, setDragOver] = useState(false);
    const action = actionCreator();
    const inputRef = useRef(null);
    const handleClick = () => {
        if (!inputRef || !inputRef.current) {
            return;
        }
        inputRef.current.click();
    };
    const handleOnChange = (e) => {
        const files = e.target.files;
        if (files === null) {
            return;
        }
        action.uploadStudyArtifact(study.id, files[0]);
    };
    const handleDragOver = (e) => {
        e.stopPropagation();
        e.preventDefault();
        e.dataTransfer.dropEffect = "copy";
        setDragOver(true);
    };
    const handleDragLeave = (e) => {
        e.stopPropagation();
        e.preventDefault();
        e.dataTransfer.dropEffect = "copy";
        setDragOver(false);
    };
    const handleDrop = (e) => {
        e.stopPropagation();
        e.preventDefault();
        const files = e.dataTransfer.files;
        setDragOver(false);
        for (let i = 0; i < files.length; i++) {
            action.uploadStudyArtifact(study.id, files[i]);
        }
    };
    return (React.createElement(Card, { sx: {
            marginBottom: theme.spacing(2),
            width: width,
            minHeight: height,
            margin: theme.spacing(0, 1, 1, 0),
            border: dragOver
                ? `3px dashed ${theme.palette.mode === "dark" ? "white" : "black"}`
                : `1px solid ${theme.palette.divider}`,
        }, onDragOver: handleDragOver, onDragLeave: handleDragLeave, onDrop: handleDrop },
        React.createElement(CardActionArea, { onClick: handleClick, sx: {
                height: "100%",
            } },
            React.createElement(CardContent, { sx: {
                    display: "flex",
                    height: "100%",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                } },
                React.createElement(UploadFileIcon, { sx: { fontSize: 80, marginBottom: theme.spacing(2) } }),
                React.createElement("input", { type: "file", ref: inputRef, onChange: handleOnChange, style: { display: "none" } }),
                React.createElement(Typography, null, "Upload a New File"),
                React.createElement(Typography, { sx: { textAlign: "center", color: theme.palette.grey.A400 } }, "Drag your file here or click to browse.")))));
};
//# sourceMappingURL=StudyArtifactCards.js.map