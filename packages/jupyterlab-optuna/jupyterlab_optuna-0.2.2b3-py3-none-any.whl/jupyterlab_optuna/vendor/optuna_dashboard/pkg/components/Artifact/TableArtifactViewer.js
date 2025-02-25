var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import ClearIcon from "@mui/icons-material/Clear";
import { Box, Modal, useTheme } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import { DataGrid } from "@optuna/react";
import { useSnackbar } from "notistack";
import Papa from "papaparse";
import React, { useState, useEffect } from "react";
import axios from "axios";
export const isTableArtifact = (artifact) => {
    return (artifact.filename.endsWith(".csv") || artifact.filename.endsWith(".jsonl"));
};
export const TableArtifactViewer = (props) => {
    const [data, setData] = useState([]);
    const { enqueueSnackbar } = useSnackbar();
    useEffect(() => {
        const handleFileChange = () => __awaiter(void 0, void 0, void 0, function* () {
            try {
                const loadedData = yield loadData(props);
                setData(loadedData);
            }
            catch (error) {
                enqueueSnackbar(`Failed to load the file. ${error}`, {
                    variant: "error",
                });
            }
        });
        handleFileChange();
    }, [props]);
    const columns = React.useMemo(() => {
        const unionSet = new Set();
        data.forEach((d) => {
            Object.keys(d).forEach((key) => {
                unionSet.add(key);
            });
        });
        const keys = Array.from(unionSet);
        return keys.map((key) => ({
            // ``header`` cannot be a falsy value, so replace key with a string looking like an empty string.
            header: key || " ",
            accessorFn: (info) => typeof info[key] === "object" ? JSON.stringify(info[key]) : info[key],
            enableSorting: true,
            enableColumnFilter: false,
        }));
    }, [data]);
    return React.createElement(DataGrid, { data: data, columns: columns, initialRowsPerPage: 10 });
};
export const useTableArtifactModal = () => {
    const [open, setOpen] = useState(false);
    const [target, setTarget] = useState(["", null]);
    const theme = useTheme();
    const openModal = (artifactUrlPath, artifact) => {
        setTarget([artifactUrlPath, artifact]);
        setOpen(true);
    };
    const renderDeleteStudyDialog = () => {
        var _a;
        return (React.createElement(Modal, { open: open, onClose: () => {
                setOpen(false);
                setTarget(["", null]);
            } },
            React.createElement(Box, { component: "div", sx: {
                    position: "absolute",
                    top: "50%",
                    left: "50%",
                    transform: "translate(-50%, -50%)",
                    bgcolor: "background.paper",
                    borderRadius: "15px",
                    width: "80%",
                    maxHeight: "80%",
                    overflowY: "auto",
                    p: 2,
                } },
                React.createElement(IconButton, { sx: {
                        position: "absolute",
                        top: theme.spacing(2),
                        right: theme.spacing(2),
                    }, onClick: () => {
                        setOpen(false);
                        setTarget(["", null]);
                    } },
                    React.createElement(ClearIcon, null)),
                React.createElement(TableArtifactViewer, { src: target[0], filetype: (_a = target[1]) === null || _a === void 0 ? void 0 : _a.filename.split(".").pop() }))));
    };
    return [openModal, renderDeleteStudyDialog];
};
const loadData = (props) => {
    if (props.filetype === "csv") {
        return loadCSV(props);
    }
    else if (props.filetype === "jsonl") {
        return loadJsonl(props);
    }
    else {
        return Promise.reject(new Error("Unsupported file type"));
    }
};
const loadCSV = (props) => {
    return new Promise((resolve, reject) => {
        Papa.parse(props.src, {
            header: true,
            download: true,
            skipEmptyLines: true,
            complete: (results) => {
                resolve(results === null || results === void 0 ? void 0 : results.data);
            },
            error: () => {
                reject(new Error("CSV parse error"));
            },
        });
    });
};
const loadJsonl = (props) => __awaiter(void 0, void 0, void 0, function* () {
    const response = yield axios.get(props.src, { responseType: "text" });
    const data = response.data;
    try {
        const jsons = data
            .split("\n")
            .filter((line) => line.trim().length > 0)
            .map((line) => {
            return JSON.parse(line);
        })
            .filter(Boolean);
        return jsons;
    }
    catch (error) {
        throw new Error("JSONL parse error");
    }
});
//# sourceMappingURL=TableArtifactViewer.js.map