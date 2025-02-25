import { TextField } from "@mui/material";
import React, { useEffect } from "react";
// TODO(c-bata): Remove this and use `useDeferredValue` instead.
export const DebouncedInputTextField = ({ onChange, delay, textFieldProps }) => {
    const [text, setText] = React.useState("");
    const [valid, setValidity] = React.useState(true);
    useEffect(() => {
        const timer = setTimeout(() => {
            onChange(text, valid);
        }, delay);
        return () => {
            clearTimeout(timer);
        };
    }, [text, delay]);
    return (React.createElement(TextField, Object.assign({ onChange: (e) => {
            setText(e.target.value);
            setValidity(e.target.validity.valid);
        } }, textFieldProps)));
};
//# sourceMappingURL=Debounce.js.map