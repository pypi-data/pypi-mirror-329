import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, useTheme, } from "@mui/material";
import React, { useState } from "react";
import { actionCreator } from "../action";
import { DebouncedInputTextField } from "./Debounce";
export const useRenameStudyDialog = (studies) => {
    const action = actionCreator();
    const theme = useTheme();
    const [openRenameStudyDialog, setOpenRenameStudyDialog] = useState(false);
    const [renameStudyID, setRenameStudyID] = useState(-1);
    const [prevStudyName, setPrevStudyName] = useState("");
    const [newStudyName, setNewStudyName] = useState("");
    const newStudyNameAlreadyUsed = studies.some((v) => v.study_name === newStudyName);
    const handleCloseRenameStudyDialog = () => {
        setOpenRenameStudyDialog(false);
        setRenameStudyID(-1);
        setPrevStudyName("");
    };
    const handleRenameStudy = () => {
        action.renameStudy(renameStudyID, newStudyName);
        setOpenRenameStudyDialog(false);
        setRenameStudyID(-1);
        setPrevStudyName("");
    };
    const openDialog = (studyId, prevStudyName) => {
        setRenameStudyID(studyId);
        setPrevStudyName(prevStudyName);
        setOpenRenameStudyDialog(true);
    };
    const renderRenameStudyDialog = () => {
        return (React.createElement(Dialog, { open: openRenameStudyDialog, onClose: () => {
                handleCloseRenameStudyDialog();
            }, "aria-labelledby": "rename-study-dialog-title" },
            React.createElement(DialogTitle, { id: "rename-study-dialog-title" },
                "Rename \"",
                prevStudyName,
                "\""),
            React.createElement(DialogContent, null,
                React.createElement(DialogContentText, { sx: {
                        fontWeight: theme.typography.fontWeightBold,
                        marginBottom: theme.spacing(1),
                    } }, "Please note that the study_id will be changed because this function internally creates a new study and copies all trials to it."),
                React.createElement(DialogContentText, null, "Please enter the new study name."),
                React.createElement(DebouncedInputTextField, { onChange: (s) => {
                        setNewStudyName(s);
                    }, delay: 500, textFieldProps: {
                        autoFocus: true,
                        fullWidth: true,
                        error: newStudyNameAlreadyUsed,
                        helperText: newStudyNameAlreadyUsed
                            ? `"${newStudyName}" is already used`
                            : "",
                        label: "Study name",
                        type: "text",
                    } })),
            React.createElement(DialogActions, null,
                React.createElement(Button, { onClick: handleCloseRenameStudyDialog, color: "primary" }, "Cancel"),
                React.createElement(Button, { onClick: handleRenameStudy, color: "primary" }, "Rename"))));
    };
    return [openDialog, renderRenameStudyDialog];
};
//# sourceMappingURL=RenameStudyDialog.js.map