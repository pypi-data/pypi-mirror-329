import { Box, Button, Card, FormControl, FormControlLabel, FormLabel, Radio, RadioGroup, Slider, TextField, Typography, useTheme, } from "@mui/material";
import React, { useMemo, useState } from "react";
import { actionCreator } from "../action";
import { useTrialUpdatingValue } from "../state";
import { DebouncedInputTextField } from "./Debounce";
export const TrialFormWidgets = ({ trial, metricNames, directions, formWidgets }) => {
    if (formWidgets === undefined ||
        trial.state === "Pruned" ||
        trial.state === "Fail") {
        return null;
    }
    const theme = useTheme();
    const trialNowUpdating = useTrialUpdatingValue(trial.trial_id);
    const headerText = formWidgets.output_type === "user_attr"
        ? "Set User Attributes Form"
        : directions.length > 1
            ? "Set Objective Values Form"
            : "Set Objective Value Form";
    const widgetNames = formWidgets.widgets.map((widget, i) => {
        if (formWidgets.output_type === "objective") {
            if (metricNames.at(i) !== undefined) {
                return metricNames[i];
            }
            return directions.length === 1 ? "Objective" : `Objective ${i}`;
        }
        else if (formWidgets.output_type === "user_attr") {
            if (widget.type !== "user_attr" && widget.user_attr_key !== undefined) {
                return widget.user_attr_key;
            }
        }
        console.error("Must not reach here");
        return "Unknown";
    });
    return (React.createElement(React.Fragment, null,
        React.createElement(Typography, { variant: "h5", sx: { fontWeight: theme.typography.fontWeightBold } }, headerText),
        trial.state === "Running" && !trialNowUpdating ? (React.createElement(UpdatableFormWidgets, { trial: trial, widgetNames: widgetNames, formWidgets: formWidgets })) : (React.createElement(ReadonlyFormWidgets, { trial: trial, widgetNames: widgetNames, formWidgets: formWidgets }))));
};
const UpdatableFormWidgets = ({ trial, widgetNames, formWidgets }) => {
    const theme = useTheme();
    const action = actionCreator();
    const widgetStates = formWidgets.widgets
        .map((w, i) => {
        const key = `${formWidgets.output_type}-${i}`;
        const outputType = formWidgets.output_type;
        if (w.type === "text") {
            return useTextInputWidget(key, outputType, w, widgetNames[i]);
        }
        else if (w.type === "choice") {
            return useChoiceWidget(key, outputType, w, widgetNames[i]);
        }
        else if (w.type === "slider") {
            return useSliderWidget(key, outputType, w, widgetNames[i]);
        }
        else if (w.type === "user_attr") {
            return useUserAttrRefWidget(key, w, widgetNames[i], trial);
        }
        console.error("Must not reach here");
        return undefined;
    })
        .filter((w) => w !== undefined);
    const disableSubmit = useMemo(() => !widgetStates.every((ws) => ws.isValid), [widgetStates]);
    const handleSubmit = (e) => {
        e.preventDefault();
        const values = widgetStates.map((ws) => ws.value);
        if (formWidgets.output_type === "objective") {
            const filtered = values.filter((v) => v !== null);
            if (filtered.length !== formWidgets.widgets.length) {
                return;
            }
            action.makeTrialComplete(trial.study_id, trial.trial_id, filtered);
        }
        else if (formWidgets.output_type === "user_attr") {
            const user_attrs = Object.fromEntries(formWidgets.widgets.map((widget, i) => [
                widget.user_attr_key,
                values[i] !== null ? values[i] : "",
            ]));
            action.saveTrialUserAttrs(trial.study_id, trial.trial_id, user_attrs);
        }
    };
    return (React.createElement(Box, { component: "div", sx: { p: theme.spacing(1, 0) } },
        React.createElement(Card, { sx: {
                display: "flex",
                flexDirection: "column",
                marginBottom: theme.spacing(2),
                margin: theme.spacing(0, 1, 1, 0),
                p: theme.spacing(1),
                maxWidth: "1000px",
            } },
            widgetStates.map((ws) => ws.render()),
            React.createElement(Box, { component: "div", sx: {
                    display: "flex",
                    flexDirection: "row",
                    margin: theme.spacing(1, 2),
                } },
                React.createElement(Button, { variant: "contained", type: "submit", sx: { marginRight: theme.spacing(1) }, disabled: disableSubmit, onClick: handleSubmit }, "Submit")))));
};
export const useTextInputWidget = (key, widgetType, widget, metricName) => {
    const theme = useTheme();
    const [value, setValue] = useState("");
    const isValid = useMemo(() => widgetType === "user_attr"
        ? value !== "" || widget.optional
        : value !== "" && !isNaN(Number(value)), [widget, value]);
    const inputProps = widgetType === "objective"
        ? {
            pattern: "[-+]?[0-9]*.?[0-9]+([eE][-+]?[0-9]+)?",
        }
        : undefined;
    const helperText = !widget.optional && value === "" ? `Please input the float number.` : "";
    const render = () => (React.createElement(FormControl, { key: key, sx: { margin: theme.spacing(1, 2) } },
        React.createElement(FormLabel, null,
            metricName,
            " - ",
            widget.description),
        React.createElement(DebouncedInputTextField, { onChange: (s, valid) => {
                if (widgetType === "user_attr") {
                    setValue(s);
                    return;
                }
                const n = Number(s);
                if (s.length > 0 && valid && !isNaN(n)) {
                    setValue(n);
                }
                else {
                    setValue("");
                }
            }, delay: 500, textFieldProps: {
                type: "text",
                autoFocus: true,
                fullWidth: true,
                required: !widget.optional,
                helperText,
                inputProps,
            } })));
    return { isValid, value, render };
};
export const useChoiceWidget = (key, widgetType, widget, metricName) => {
    const theme = useTheme();
    const [value, setValue] = useState(widget.values[0]);
    const render = () => (React.createElement(FormControl, { key: key, sx: { margin: theme.spacing(1, 2) } },
        React.createElement(FormLabel, null,
            metricName,
            " - ",
            widget.description),
        React.createElement(RadioGroup, { row: true, defaultValue: widget.values.at(0) }, widget.choices.map((c, j) => (React.createElement(FormControlLabel, { key: c, control: React.createElement(Radio, { checked: value === widget.values.at(j), onChange: (e) => {
                    const selected = widget.values.at(j);
                    if (selected === undefined) {
                        console.error("Must not reach here.");
                        return;
                    }
                    if (e.target.checked) {
                        setValue(selected);
                    }
                } }), label: c }))))));
    return { isValid: true, value, render };
};
export const useSliderWidget = (key, widgetType, widget, metricName) => {
    const theme = useTheme();
    const [value, setValue] = useState(widget.min);
    const defaultStep = 0.01;
    const render = () => (React.createElement(FormControl, { key: key, sx: { margin: theme.spacing(1, 2) } },
        React.createElement(FormLabel, null,
            metricName,
            " - ",
            widget.description),
        React.createElement(Box, { component: "div", sx: { padding: theme.spacing(0, 2) } },
            React.createElement(Slider, { onChange: (e) => {
                    // @ts-ignore
                    setValue(e.target.value);
                }, defaultValue: widget.min, min: widget.min, max: widget.max, step: widget.step || defaultStep, marks: widget.labels === null ? undefined : widget.labels, valueLabelDisplay: "auto" }))));
    return { isValid: true, value, render };
};
export const useUserAttrRefWidget = (key, widget, metricName, trial) => {
    const theme = useTheme();
    const value = useMemo(() => {
        const attr = trial.user_attrs.find((attr) => attr.key === widget.key);
        if (attr === undefined) {
            return null;
        }
        const n = Number(attr.value);
        if (isNaN(n)) {
            return null;
        }
        return n;
    }, [trial.user_attrs]);
    const render = () => (React.createElement(FormControl, { key: key, sx: { margin: theme.spacing(1, 2) } },
        React.createElement(FormLabel, null, metricName),
        React.createElement(TextField, { inputProps: { readOnly: true }, value: value || "", error: value === null, helperText: value === null
                ? `This objective value is referred from trial.user_attrs[${widget.key}].`
                : "" })));
    return {
        isValid: value !== null,
        value: value !== null ? value : "",
        render,
    };
};
const ReadonlyFormWidgets = ({ trial, widgetNames, formWidgets }) => {
    const theme = useTheme();
    const getValue = (i) => {
        var _a, _b;
        if (formWidgets.output_type === "user_attr") {
            const widget = formWidgets.widgets[i];
            return (((_a = trial.user_attrs.find((attr) => attr.key === widget.user_attr_key)) === null || _a === void 0 ? void 0 : _a.value) || "");
        }
        const value = (_b = trial.values) === null || _b === void 0 ? void 0 : _b.at(i);
        if (value === undefined) {
            console.error("Must not reach here.");
            return 0;
        }
        return value;
    };
    if (trial.state !== "Complete") {
        return null;
    }
    return (React.createElement(Box, { component: "div", sx: { p: theme.spacing(1, 0) } },
        React.createElement(Card, { sx: {
                display: "flex",
                flexDirection: "column",
                marginBottom: theme.spacing(2),
                margin: theme.spacing(0, 1, 1, 0),
                p: theme.spacing(1),
                maxWidth: "1000px",
            } }, formWidgets.widgets.map((widget, i) => {
            var _a, _b, _c;
            const key = `objective-${i}`;
            const widgetName = widgetNames[i];
            if (widget.type === "text") {
                return (React.createElement(FormControl, { key: key, sx: { margin: theme.spacing(1, 2) } },
                    React.createElement(FormLabel, null,
                        widgetName,
                        " - ",
                        widget.description),
                    React.createElement(TextField, { inputProps: { readOnly: true }, value: getValue(i) })));
            }
            else if (widget.type === "choice") {
                return (React.createElement(FormControl, { key: key, sx: { margin: theme.spacing(1, 2) } },
                    React.createElement(FormLabel, null,
                        widgetName,
                        " - ",
                        widget.description),
                    React.createElement(RadioGroup, { row: true, defaultValue: (_a = trial.values) === null || _a === void 0 ? void 0 : _a.at(i) }, widget.choices.map((c, j) => {
                        var _a;
                        return (React.createElement(FormControlLabel, { key: c, control: React.createElement(Radio, { checked: ((_a = trial.values) === null || _a === void 0 ? void 0 : _a.at(i)) === widget.values.at(j) }), label: c, disabled: true }));
                    }))));
            }
            else if (widget.type === "slider") {
                const value = (_b = trial.values) === null || _b === void 0 ? void 0 : _b.at(i);
                return (React.createElement(FormControl, { key: key, sx: { margin: theme.spacing(1, 2) } },
                    React.createElement(FormLabel, null,
                        widgetName,
                        " - ",
                        widget.description),
                    React.createElement(Box, { component: "div", sx: { padding: theme.spacing(0, 2) } },
                        React.createElement(Slider, { defaultValue: value, min: widget.min, max: widget.max, step: widget.step, marks: widget.labels === null || widget.labels.length === 0
                                ? true
                                : widget.labels, valueLabelDisplay: "auto", disabled: true }))));
            }
            else if (widget.type === "user_attr") {
                return (React.createElement(FormControl, { key: key, sx: { margin: theme.spacing(1, 2) } },
                    React.createElement(FormLabel, null, widgetName),
                    React.createElement(TextField, { inputProps: { readOnly: true }, value: (_c = trial.values) === null || _c === void 0 ? void 0 : _c.at(i), disabled: true })));
            }
            return null;
        }))));
};
//# sourceMappingURL=TrialFormWidgets.js.map