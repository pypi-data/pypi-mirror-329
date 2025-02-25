import { Alert, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, useTheme, } from "@mui/material";
import React, { useState } from "react";
import { actionCreator } from "../../action";
export const useDeleteTrialArtifactDialog = () => {
    const action = actionCreator();
    const [openDeleteArtifactDialog, setOpenDeleteArtifactDialog] = useState(false);
    const [target, setTarget] = useState([
        -1,
        -1,
        null,
    ]);
    const handleCloseDeleteArtifactDialog = () => {
        setOpenDeleteArtifactDialog(false);
        setTarget([-1, -1, null]);
    };
    const handleDeleteArtifact = () => {
        const [studyId, trialId, artifact] = target;
        if (artifact === null) {
            return;
        }
        action.deleteTrialArtifact(studyId, trialId, artifact.artifact_id);
        setOpenDeleteArtifactDialog(false);
        setTarget([-1, -1, null]);
    };
    const openDialog = (studyId, trialId, artifact) => {
        setTarget([studyId, trialId, artifact]);
        setOpenDeleteArtifactDialog(true);
    };
    const renderDeleteArtifactDialog = () => {
        var _a;
        return (React.createElement(DeleteDialog, { openDeleteArtifactDialog: openDeleteArtifactDialog, handleCloseDeleteArtifactDialog: handleCloseDeleteArtifactDialog, filename: (_a = target[2]) === null || _a === void 0 ? void 0 : _a.filename, handleDeleteArtifact: handleDeleteArtifact }));
    };
    return [openDialog, renderDeleteArtifactDialog];
};
export const useDeleteStudyArtifactDialog = () => {
    const action = actionCreator();
    const [openDeleteArtifactDialog, setOpenDeleteArtifactDialog] = useState(false);
    const [target, setTarget] = useState([-1, null]);
    const handleCloseDeleteArtifactDialog = () => {
        setOpenDeleteArtifactDialog(false);
        setTarget([-1, null]);
    };
    const handleDeleteArtifact = () => {
        const [studyId, artifact] = target;
        if (artifact === null) {
            return;
        }
        action.deleteStudyArtifact(studyId, artifact.artifact_id);
        setOpenDeleteArtifactDialog(false);
        setTarget([-1, null]);
    };
    const openDialog = (studyId, artifact) => {
        setTarget([studyId, artifact]);
        setOpenDeleteArtifactDialog(true);
    };
    const renderDeleteArtifactDialog = () => {
        var _a;
        return (React.createElement(DeleteDialog, { openDeleteArtifactDialog: openDeleteArtifactDialog, handleCloseDeleteArtifactDialog: handleCloseDeleteArtifactDialog, filename: (_a = target[1]) === null || _a === void 0 ? void 0 : _a.filename, handleDeleteArtifact: handleDeleteArtifact }));
    };
    return [openDialog, renderDeleteArtifactDialog];
};
const DeleteDialog = ({ openDeleteArtifactDialog, handleCloseDeleteArtifactDialog, filename, handleDeleteArtifact, }) => {
    const theme = useTheme();
    return (React.createElement(Dialog, { open: openDeleteArtifactDialog, onClose: () => {
            handleCloseDeleteArtifactDialog();
        }, "aria-labelledby": "delete-artifact-dialog-title" },
        React.createElement(DialogTitle, { id: "delete-artifact-dialog-title" }, "Delete artifact"),
        React.createElement(DialogContent, null,
            React.createElement(DialogContentText, { sx: {
                    marginBottom: theme.spacing(2),
                } },
                "Are you sure you want to delete an artifact (\"",
                filename,
                "\")?"),
            React.createElement(Alert, { severity: "warning" }, "If this artifact is linked to another study or trial, it will no longer be accessible from that study or trial as well.")),
        React.createElement(DialogActions, null,
            React.createElement(Button, { onClick: handleCloseDeleteArtifactDialog, color: "primary" }, "No"),
            React.createElement(Button, { onClick: handleDeleteArtifact, color: "primary" }, "Yes"))));
};
//# sourceMappingURL=DeleteArtifactDialog.js.map