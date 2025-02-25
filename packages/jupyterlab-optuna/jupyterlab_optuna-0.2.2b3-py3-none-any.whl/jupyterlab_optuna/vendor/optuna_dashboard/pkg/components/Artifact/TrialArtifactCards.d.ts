import { FC } from "react";
import { Trial } from "ts/types/optuna";
export declare const getTrialArtifactUrlPath: (baseUrlPath: string, studyId: number, trialId: number, artifactId: string) => string;
export declare const TrialArtifactCards: FC<{
    trial: Trial;
}>;
