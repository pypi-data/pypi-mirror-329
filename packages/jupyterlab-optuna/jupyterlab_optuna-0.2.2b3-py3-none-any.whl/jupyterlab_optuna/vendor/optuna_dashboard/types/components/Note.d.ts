import { SxProps } from "@mui/material";
import { Theme } from "@mui/material/styles";
import { FC } from "react";
import { Note } from "ts/types/optuna";
export declare const TrialNote: FC<{
    studyId: number;
    trialId: number;
    latestNote: Note;
    cardSx?: SxProps<Theme>;
}>;
export declare const StudyNote: FC<{
    studyId: number;
    latestNote: Note;
    cardSx?: SxProps<Theme>;
}>;
export declare const MarkdownRenderer: FC<{
    body: string;
}>;
