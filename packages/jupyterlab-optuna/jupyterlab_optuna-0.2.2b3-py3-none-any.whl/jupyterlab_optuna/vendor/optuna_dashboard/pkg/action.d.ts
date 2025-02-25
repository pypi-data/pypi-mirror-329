import * as Optuna from "@optuna/types";
import { FeedbackComponentType, Note } from "./types/optuna";
export declare const actionCreator: () => {
    updateAPIMeta: () => void;
    updateStudyDetail: (studyId: number) => void;
    updateStudySummaries: (successMsg?: string) => void;
    createNewStudy: (studyName: string, directions: Optuna.StudyDirection[]) => void;
    deleteStudy: (studyId: number, removeAssociatedArtifacts: boolean) => void;
    renameStudy: (studyId: number, studyName: string) => void;
    saveReloadInterval: (interval: number) => void;
    saveStudyNote: (studyId: number, note: Note) => Promise<void>;
    saveTrialNote: (studyId: number, trialId: number, note: Note) => Promise<void>;
    uploadTrialArtifact: (studyId: number, trialId: number, file: File) => void;
    uploadStudyArtifact: (studyId: number, file: File) => void;
    deleteTrialArtifact: (studyId: number, trialId: number, artifactId: string) => void;
    deleteStudyArtifact: (studyId: number, artifactId: string) => void;
    makeTrialComplete: (studyId: number, trialId: number, values: number[]) => void;
    makeTrialFail: (studyId: number, trialId: number) => void;
    saveTrialUserAttrs: (studyId: number, trialId: number, user_attrs: {
        [key: string]: string | number;
    }) => void;
    updatePreference: (studyId: number, candidates: number[], clicked: number) => void;
    skipPreferentialTrial: (studyId: number, trialId: number) => void;
    removePreferentialHistory: (studyId: number, historyId: string) => void;
    restorePreferentialHistory: (studyId: number, historyId: string) => void;
    updateFeedbackComponent: (studyId: number, compoennt_type: FeedbackComponentType) => void;
};
export type Action = ReturnType<typeof actionCreator>;
