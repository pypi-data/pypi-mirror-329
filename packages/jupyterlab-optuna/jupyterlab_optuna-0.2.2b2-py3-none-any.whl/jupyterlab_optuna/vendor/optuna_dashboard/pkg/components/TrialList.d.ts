import * as Optuna from "@optuna/types";
import { FC } from "react";
import { FormWidgets, StudyDetail, Trial } from "ts/types/optuna";
export declare const TrialListDetail: FC<{
    trial: Trial;
    isBestTrial: (trialId: number) => boolean;
    directions: Optuna.StudyDirection[];
    metricNames: string[];
    formWidgets?: FormWidgets;
}>;
export declare const TrialList: FC<{
    studyDetail: StudyDetail | null;
}>;
