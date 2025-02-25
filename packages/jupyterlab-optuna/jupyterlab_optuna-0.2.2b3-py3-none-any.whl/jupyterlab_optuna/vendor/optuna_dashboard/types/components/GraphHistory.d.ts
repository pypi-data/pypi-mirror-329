import { FC } from "react";
import { StudyDetail } from "ts/types/optuna";
export declare const GraphHistory: FC<{
    studies: StudyDetail[];
    logScale: boolean;
    includePruned: boolean;
}>;
