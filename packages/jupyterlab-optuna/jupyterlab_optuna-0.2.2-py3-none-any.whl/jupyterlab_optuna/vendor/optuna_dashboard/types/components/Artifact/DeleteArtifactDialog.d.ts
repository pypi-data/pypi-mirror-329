import { ReactNode } from "react";
import { Artifact } from "ts/types/optuna";
export declare const useDeleteTrialArtifactDialog: () => [(studyId: number, trialId: number, artifact: Artifact) => void, () => ReactNode];
export declare const useDeleteStudyArtifactDialog: () => [(studyId: number, artifact: Artifact) => void, () => ReactNode];
