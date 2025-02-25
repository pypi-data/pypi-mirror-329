import { Alert, Button, Checkbox, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, FormControlLabel, } from "@mui/material";
import React, { useState } from "react";
import { useRecoilValue } from "recoil";
import { actionCreator } from "../action";
import { artifactIsAvailable as artifactIsAvailableState } from "../state";
export const useDeleteStudyDialog = () => {
    const action = actionCreator();
    const artifactIsAvailable = useRecoilValue(artifactIsAvailableState);
    const [openDeleteStudyDialog, setOpenDeleteStudyDialog] = useState(false);
    const [deleteStudyID, setDeleteStudyID] = useState(-1);
    const [removeAssociatedArtifacts, setRemoveAssociatedArtifacts] = useState(false);
    const handleCloseDeleteStudyDialog = () => {
        setOpenDeleteStudyDialog(false);
        setDeleteStudyID(-1);
        setRemoveAssociatedArtifacts(false);
    };
    const handleDeleteStudy = () => {
        action.deleteStudy(deleteStudyID, removeAssociatedArtifacts);
        handleCloseDeleteStudyDialog();
    };
    const openDialog = (studyId) => {
        setDeleteStudyID(studyId);
        setOpenDeleteStudyDialog(true);
    };
    const renderDeleteStudyDialog = () => {
        return (React.createElement(Dialog, { open: openDeleteStudyDialog, onClose: () => {
                handleCloseDeleteStudyDialog();
            }, "aria-labelledby": "delete-study-dialog-title", fullWidth: true, maxWidth: "xs" },
            React.createElement(DialogTitle, { id: "delete-study-dialog-title" }, "Delete study"),
            React.createElement(DialogContent, null,
                React.createElement(DialogContentText, null,
                    "Are you sure you want to delete a study (id=",
                    deleteStudyID,
                    ")?"),
                artifactIsAvailable && (React.createElement(React.Fragment, null,
                    React.createElement(FormControlLabel, { label: "Remove associated trial/study artifacts.", control: React.createElement(Checkbox, { checked: removeAssociatedArtifacts, onChange: () => setRemoveAssociatedArtifacts((cur) => !cur) }) }),
                    removeAssociatedArtifacts && (React.createElement(Alert, { severity: "warning" }, "If artifacts are linked to another study or trial, they will no longer be accessible from that study or trial as well."))))),
            React.createElement(DialogActions, null,
                React.createElement(Button, { onClick: handleCloseDeleteStudyDialog, color: "primary" }, "No"),
                React.createElement(Button, { onClick: handleDeleteStudy, color: "primary" }, "Yes"))));
    };
    return [openDialog, renderDeleteStudyDialog];
};
//# sourceMappingURL=DeleteStudyDialog.js.map