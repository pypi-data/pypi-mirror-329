import { FC } from "react";
import { Artifact, FeedbackComponentType, Trial } from "ts/types/optuna";
export declare const PreferentialOutputComponent: FC<{
    trial: Trial;
    artifact?: Artifact;
    componentType: FeedbackComponentType;
    urlPath: string;
}>;
