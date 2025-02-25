import { TextFieldProps } from "@mui/material";
import { FC } from "react";
export declare const DebouncedInputTextField: FC<{
    onChange: (s: string, valid: boolean) => void;
    delay: number;
    textFieldProps: TextFieldProps;
}>;
