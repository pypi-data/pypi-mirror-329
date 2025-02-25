var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
import CloseIcon from "@mui/icons-material/Close";
import EditIcon from "@mui/icons-material/Edit";
import HtmlIcon from "@mui/icons-material/Html";
import ModeEditIcon from "@mui/icons-material/ModeEdit";
import SaveIcon from "@mui/icons-material/Save";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import LoadingButton from "@mui/lab/LoadingButton";
import { Box, Button, Card, CardContent, CardHeader, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, IconButton, ImageList, ImageListItem, ImageListItemBar, TextField, Typography, useTheme, } from "@mui/material";
import React, { createRef, useState, useEffect, useRef, } from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { darcula } from "react-syntax-highlighter/dist/esm/styles/prism";
// @ts-ignore
import rehypeMathjax from "rehype-mathjax";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import { useRecoilValue } from "recoil";
import { actionCreator } from "../action";
import { artifactIsAvailable, isFileUploading, useArtifacts } from "../state";
const placeholder = `## What is this feature for?

Here you can freely take a note in *(GitHub flavored) Markdown format*.
In addition, **code blocks with syntax highlights** and **formula** are also supported here, as shown below.

### Code-block with Syntax Highlights

\`\`\`python
def objective(trial):
    x = trial.suggest_float("x", -10, 10)
    y = trial.suggest_float("y", -10, 10)
    return (x - 5) ** 2 + (y + 5) ** 2
\`\`\`

### Formula

$$
L = \\frac{1}{2} \\rho v^2 S C_L
$$
`;
const CodeBlock = (_a) => {
    var { 
    // @ts-ignore
    inline, 
    // @ts-ignore
    className, 
    // @ts-ignore
    children } = _a, props = __rest(_a, ["inline", "className", "children"]);
    const match = /language-(\w+)/.exec(className || "");
    return !inline && match ? (React.createElement(SyntaxHighlighter, Object.assign({ style: darcula, language: match[1], PreTag: "div" }, props), String(children).replace(/\n$/, ""))) : (React.createElement("code", Object.assign({ className: className }, props), children));
};
export const TrialNote = ({ studyId, trialId, latestNote, cardSx }) => {
    return (React.createElement(NoteBase, { studyId: studyId, trialId: trialId, latestNote: latestNote, cardSx: cardSx }));
};
export const StudyNote = ({ studyId, latestNote, cardSx }) => {
    return React.createElement(NoteBase, { studyId: studyId, latestNote: latestNote, cardSx: cardSx });
};
const useConfirmCloseDialog = (handleClose) => {
    const theme = useTheme();
    const [open, setOpen] = useState(false);
    const zIndex = theme.zIndex.snackbar - 1;
    const openDialog = () => {
        setOpen(true);
    };
    const renderDialog = () => {
        return (React.createElement(Dialog, { open: open, sx: {
                zIndex: zIndex,
            } },
            React.createElement(DialogTitle, null, "Unsaved changes"),
            React.createElement(DialogContent, null,
                React.createElement(DialogContentText, null, "Do you want to save or discard your changes?")),
            React.createElement(DialogActions, null,
                React.createElement(Button, { onClick: handleClose, color: "primary" }, "Discard"),
                React.createElement(Button, { onClick: () => {
                        setOpen(false);
                    }, color: "primary" }, "Stay"))));
    };
    return [openDialog, renderDialog];
};
export const MarkdownRenderer = ({ body }) => (React.createElement(ReactMarkdown, { children: body, remarkPlugins: [remarkGfm, remarkMath], rehypePlugins: [rehypeMathjax, rehypeRaw], components: {
        code: CodeBlock,
        img: (props) => React.createElement("img", Object.assign({}, props, { style: { maxWidth: "100%" } })),
    } }));
const MarkdownEditorModal = ({ studyId, trialId, latestNote, setEditorUnmount }) => {
    const theme = useTheme();
    const action = actionCreator();
    const [openConfirmCloseDialog, renderConfirmCloseDialog] = useConfirmCloseDialog(() => {
        setEditorUnmount();
        window.onbeforeunload = null;
    });
    const [saving, setSaving] = useState(false);
    const [edited, setEdited] = useState(false);
    const [curNote, setCurNote] = useState({ version: 0, body: "" });
    const textAreaRef = createRef();
    const notLatest = latestNote.version > curNote.version;
    const artifactEnabled = useRecoilValue(artifactIsAvailable);
    const [previewMarkdown, setPreviewMarkdown] = useState("");
    const [preview, setPreview] = useState(false);
    useEffect(() => {
        setCurNote(latestNote);
    }, []);
    useEffect(() => {
        if (edited) {
            window.onbeforeunload = (e) => {
                e.returnValue = "Are you okay to discard your changes?";
            };
        }
        else {
            window.onbeforeunload = null;
        }
    }, [edited]);
    const handleSave = () => {
        const nextVersion = curNote.version + 1;
        const newNote = {
            version: nextVersion,
            body: textAreaRef.current ? textAreaRef.current.value : "",
        };
        setSaving(true);
        let actionResponse;
        if (trialId === undefined) {
            actionResponse = action.saveStudyNote(studyId, newNote);
        }
        else {
            actionResponse = action.saveTrialNote(studyId, trialId, newNote);
        }
        actionResponse
            .then(() => {
            setCurNote(newNote);
            window.onbeforeunload = null;
            setEditorUnmount();
        })
            .finally(() => {
            setSaving(false);
        });
    };
    const handleRefresh = () => {
        if (!textAreaRef.current) {
            console.log("Unexpectedly, textarea is not found.");
            return;
        }
        textAreaRef.current.value = latestNote.body;
        setCurNote(latestNote);
        window.onbeforeunload = null;
    };
    const insertTextFromCursorPoint = (text) => {
        if (textAreaRef.current === null) {
            return;
        }
        const cursorPosition = textAreaRef.current.selectionStart;
        const currentBody = textAreaRef.current.value;
        textAreaRef.current.value =
            currentBody.substring(0, cursorPosition) +
                text +
                currentBody.substring(cursorPosition, currentBody.length);
        setEdited(true);
    };
    // See https://github.com/iamhosseindhv/notistack/issues/231#issuecomment-825924840
    const zIndex = theme.zIndex.snackbar - 2;
    return (React.createElement(Card, { sx: {
            bottom: 0,
            height: "100%",
            left: 0,
            overflow: "scroll",
            position: "fixed",
            right: 0,
            top: 0,
            zIndex: zIndex,
            p: theme.spacing(2),
            display: "flex",
            flexDirection: "column",
        } },
        React.createElement(CardHeader, { action: React.createElement(IconButton, { onClick: () => {
                    setPreview(!preview);
                    setPreviewMarkdown(textAreaRef.current ? textAreaRef.current.value : "");
                } }, preview ? (React.createElement(ModeEditIcon, { color: "primary" })) : (React.createElement(HtmlIcon, { color: "primary" }))), title: "Markdown Editor" }),
        React.createElement(Box, { component: "div", sx: {
                flexGrow: 1,
                padding: theme.spacing(2),
                display: preview ? "default" : "none",
                overflow: "scroll",
            } },
            React.createElement(MarkdownRenderer, { body: previewMarkdown })),
        React.createElement(Box, { component: "div", sx: {
                width: "100%",
                flexGrow: 1,
                display: preview ? "none" : "flex",
                flexDirection: "row",
                margin: theme.spacing(1, 0),
            } },
            React.createElement(TextField, { disabled: saving, multiline: true, placeholder: placeholder, sx: {
                    position: "relative",
                    resize: "none",
                    width: "100%",
                    height: "100%",
                    "& .MuiInputBase-root": {
                        height: "100%",
                        alignItems: "start",
                    },
                }, inputRef: textAreaRef, defaultValue: latestNote.body, onChange: () => {
                    const cur = textAreaRef.current ? textAreaRef.current.value : "";
                    if (edited !== (cur !== curNote.body)) {
                        setEdited(cur !== curNote.body);
                    }
                } }),
            artifactEnabled && trialId !== undefined && (React.createElement(ArtifactUploader, { studyId: studyId, trialId: trialId, insert: insertTextFromCursorPoint }))),
        React.createElement(Box, { component: "div", sx: { display: "flex", flexDirection: "row", alignItems: "center" } },
            notLatest && !saving && (React.createElement(React.Fragment, null,
                React.createElement(Typography, { sx: {
                        color: theme.palette.error.main,
                        fontSize: "0.8rem",
                        display: "inline",
                    } }, "The text you are editing has updated. Do you want to discard your changes and refresh the textarea?"),
                React.createElement(Button, { variant: "text", onClick: handleRefresh, color: "error", size: "small", sx: { textDecoration: "underline" } }, "Yes"))),
            React.createElement(Box, { component: "div", sx: { flexGrow: 1 } }),
            React.createElement(Button, { variant: "outlined", onClick: () => {
                    if (edited) {
                        openConfirmCloseDialog();
                    }
                    else {
                        setEditorUnmount();
                    }
                }, startIcon: React.createElement(CloseIcon, null) }, "Close"),
            React.createElement(LoadingButton, { onClick: handleSave, loading: saving, loadingPosition: "start", startIcon: React.createElement(SaveIcon, null), variant: "contained", disabled: !edited || notLatest, sx: { marginLeft: theme.spacing(1) } }, "Save")),
        renderConfirmCloseDialog()));
};
const ArtifactUploader = ({ studyId, trialId, insert }) => {
    const theme = useTheme();
    const action = actionCreator();
    const uploading = useRecoilValue(isFileUploading);
    const artifacts = useArtifacts(studyId, trialId);
    const [dragOver, setDragOver] = useState(false);
    const [selectedArtifactId, setSelectedArtifactId] = useState("");
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
        action.uploadTrialArtifact(studyId, trialId, files[0]);
    };
    const handleDrop = (e) => {
        e.stopPropagation();
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        setDragOver(false);
        action.uploadTrialArtifact(studyId, trialId, file);
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
    return (React.createElement(Box, { component: "div", sx: {
            width: "300px",
            padding: theme.spacing(0, 1),
            display: "flex",
            flexDirection: "column",
        }, onDragOver: handleDragOver, onDragLeave: handleDragLeave, onDrop: handleDrop },
        React.createElement(Typography, { sx: {
                fontWeight: theme.typography.fontWeightBold,
                margin: theme.spacing(1, 0),
            } }, "Image"),
        React.createElement(LoadingButton, { loading: uploading, loadingPosition: "start", startIcon: React.createElement(UploadFileIcon, null), onClick: handleClick, variant: "outlined" }, "Upload"),
        React.createElement("input", { type: "file", ref: inputRef, onChange: handleOnChange, style: { display: "none" } }),
        React.createElement(Box, { component: "div", sx: {
                border: dragOver
                    ? `3px dashed ${theme.palette.mode === "dark" ? "white" : "black"}`
                    : `1px solid ${theme.palette.divider}`,
                margin: theme.spacing(1, 0),
                borderRadius: "4px",
                flexGrow: 1,
                flexBasis: 0,
                overflow: "scroll",
            } },
            dragOver && (React.createElement(Box, { component: "div", sx: {
                    width: "100%",
                    height: "100%",
                    position: "relative",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                    backgroundColor: theme.palette.mode === "dark"
                        ? "rgba(255, 255, 255, 0.3)"
                        : "rgba(0,0,0,0.3)",
                } },
                React.createElement(UploadFileIcon, { sx: { fontSize: 80, marginBottom: theme.spacing(2) } }),
                React.createElement(Typography, null, "Upload a New Image"),
                React.createElement(Typography, { sx: { textAlign: "center", color: theme.palette.grey.A400 } }, "Drag your file here."))),
            React.createElement(ImageList, { cols: 1, sx: { margin: 0 } }, artifacts
                .filter((a) => a.mimetype.startsWith("image"))
                .map((a) => (React.createElement(ImageListItem, { key: a.artifact_id, onClick: () => {
                    if (selectedArtifactId === a.artifact_id) {
                        setSelectedArtifactId("");
                    }
                    else {
                        setSelectedArtifactId(a.artifact_id);
                    }
                }, sx: {
                    border: selectedArtifactId === a.artifact_id
                        ? `2px solid ${theme.palette.primary.main}`
                        : "none",
                } },
                React.createElement("img", { src: `/artifacts/${studyId}/${trialId}/${a.artifact_id}` }),
                React.createElement(ImageListItemBar, { title: a.filename })))))),
        React.createElement(Button, { variant: "outlined", disabled: selectedArtifactId === "", onClick: () => {
                if (selectedArtifactId === "") {
                    return;
                }
                const artifact = artifacts.find((a) => a.artifact_id === selectedArtifactId);
                if (artifact === undefined) {
                    return;
                }
                insert(`![${artifact.filename}](/artifacts/${studyId}/${trialId}/${artifact.artifact_id})\n`);
                setSelectedArtifactId("");
            } }, "Insert an image")));
};
const NoteBase = ({ studyId, trialId, latestNote, cardSx }) => {
    const theme = useTheme();
    const [editorMounted, setEditorMounted] = useState(false);
    const defaultBody = "";
    return (React.createElement(Card, { sx: Object.assign({ overflow: "scroll" }, cardSx) },
        React.createElement(CardContent, { sx: {
                paddingTop: theme.spacing(1),
                position: "relative",
                minHeight: theme.spacing(7),
            } },
            React.createElement(MarkdownRenderer, { body: latestNote.body || defaultBody }),
            React.createElement(IconButton, { sx: {
                    position: "absolute",
                    top: 0,
                    right: 0,
                    margin: theme.spacing(1),
                }, onClick: () => {
                    setEditorMounted(true);
                } },
                React.createElement(EditIcon, null))),
        editorMounted && (React.createElement(MarkdownEditorModal, { studyId: studyId, trialId: trialId, latestNote: latestNote, setEditorUnmount: () => {
                setEditorMounted(false);
            } }))));
};
//# sourceMappingURL=Note.js.map