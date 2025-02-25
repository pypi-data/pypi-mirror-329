import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, FormControl, FormLabel, MenuItem, Select, useTheme, } from "@mui/material";
import React, { useState } from "react";
import { useRecoilValue } from "recoil";
import { actionCreator } from "../action";
import { studySummariesState } from "../state";
import { DebouncedInputTextField } from "./Debounce";
export const useCreateStudyDialog = () => {
    const theme = useTheme();
    const action = actionCreator();
    const [newStudyName, setNewStudyName] = useState("");
    const [openNewStudyDialog, setOpenNewStudyDialog] = useState(false);
    const [directions, setDirections] = useState([
        "minimize",
    ]);
    const studies = useRecoilValue(studySummariesState);
    const newStudyNameAlreadyUsed = studies.some((v) => v.study_name === newStudyName);
    const handleCloseNewStudyDialog = () => {
        setOpenNewStudyDialog(false);
        setNewStudyName("");
        setDirections(["minimize"]);
    };
    const handleCreateNewStudy = () => {
        action.createNewStudy(newStudyName, directions);
        setOpenNewStudyDialog(false);
        setNewStudyName("");
        setDirections(["minimize"]);
    };
    const openDialog = () => {
        setOpenNewStudyDialog(true);
    };
    const renderCreateNewStudyDialog = () => {
        return (React.createElement(Dialog, { open: openNewStudyDialog, onClose: () => {
                handleCloseNewStudyDialog();
            }, "aria-labelledby": "create-study-dialog-title" },
            React.createElement(DialogTitle, { id: "create-study-dialog-title" }, "New Study"),
            React.createElement(DialogContent, null,
                React.createElement(DialogContentText, null, "Please enter the study name and directions here."),
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
            directions.map((d, i) => (React.createElement(DialogContent, { key: i },
                React.createElement(FormControl, { component: "fieldset", fullWidth: true },
                    React.createElement(FormLabel, { component: "legend" },
                        "Objective ",
                        i,
                        ":"),
                    React.createElement(Select, { value: directions[i], onChange: (e) => {
                            const newVal = [...directions];
                            newVal[i] = e.target.value;
                            setDirections(newVal);
                        } },
                        React.createElement(MenuItem, { value: "minimize" }, "Minimize"),
                        React.createElement(MenuItem, { value: "maximize" }, "Maximize")))))),
            React.createElement(DialogContent, null,
                React.createElement(Button, { variant: "outlined", startIcon: React.createElement(AddIcon, null), sx: { marginRight: theme.spacing(1) }, onClick: () => {
                        const newVal = [
                            ...directions,
                            "minimize",
                        ];
                        setDirections(newVal);
                    } }, "Add"),
                React.createElement(Button, { variant: "outlined", startIcon: React.createElement(RemoveIcon, null), sx: { marginRight: theme.spacing(1) }, disabled: directions.length <= 1, onClick: () => {
                        const newVal = [...directions];
                        newVal.pop();
                        setDirections(newVal);
                    } }, "Remove")),
            React.createElement(DialogActions, null,
                React.createElement(Button, { onClick: handleCloseNewStudyDialog, color: "primary" }, "Cancel"),
                React.createElement(Button, { onClick: handleCreateNewStudy, color: "primary", disabled: newStudyName === "" ||
                        newStudyNameAlreadyUsed ||
                        directions.length === 0 }, "Create"))));
    };
    return [openDialog, renderCreateNewStudyDialog];
};
//# sourceMappingURL=CreateStudyDialog.js.map