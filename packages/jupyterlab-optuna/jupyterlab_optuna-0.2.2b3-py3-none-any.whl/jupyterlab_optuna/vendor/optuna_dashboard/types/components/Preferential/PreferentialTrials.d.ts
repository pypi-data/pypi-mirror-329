import { FC } from "react";
import { StudyDetail } from "ts/types/optuna";
export declare const getArtifactUrlPath: (studyId: number, trialId: number, artifactId: string) => string;
export declare const PreferentialTrials: FC<{
    studyDetail: StudyDetail | null;
}>;
