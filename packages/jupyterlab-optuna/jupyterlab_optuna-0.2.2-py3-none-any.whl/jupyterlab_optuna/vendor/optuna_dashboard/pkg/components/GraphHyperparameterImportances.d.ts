import { FC } from "react";
import { StudyDetail } from "ts/types/optuna";
export declare const GraphHyperparameterImportance: FC<{
    studyId: number;
    study: StudyDetail | null;
    graphHeight: string;
}>;
