import * as Optuna from "@optuna/types";
import { APIClient, APIMeta, CompareStudiesPlotType, PlotResponse, PlotType, UploadArtifactAPIResponse } from "./apiClient";
import { FeedbackComponentType, ParamImportance, StudyDetail, StudySummary } from "./types/optuna";
export declare class AxiosClient extends APIClient {
    private axiosInstance;
    constructor();
    getMetaInfo: () => Promise<APIMeta>;
    getStudyDetail: (studyId: number, nLocalTrials: number) => Promise<StudyDetail>;
    getStudySummaries: () => Promise<StudySummary[]>;
    createNewStudy: (studyName: string, directions: Optuna.StudyDirection[]) => Promise<StudySummary>;
    deleteStudy: (studyId: number, removeAssociatedArtifacts: boolean) => Promise<void>;
    renameStudy: (studyId: number, studyName: string) => Promise<StudySummary>;
    saveStudyNote: (studyId: number, note: {
        version: number;
        body: string;
    }) => Promise<void>;
    saveTrialNote: (studyId: number, trialId: number, note: {
        version: number;
        body: string;
    }) => Promise<void>;
    uploadTrialArtifact: (studyId: number, trialId: number, fileName: string, dataUrl: string) => Promise<UploadArtifactAPIResponse>;
    uploadStudyArtifact: (studyId: number, fileName: string, dataUrl: string) => Promise<UploadArtifactAPIResponse>;
    deleteTrialArtifact: (studyId: number, trialId: number, artifactId: string) => Promise<void>;
    deleteStudyArtifact: (studyId: number, artifactId: string) => Promise<void>;
    tellTrial: (trialId: number, state: Optuna.TrialStateFinished, values?: number[]) => Promise<void>;
    saveTrialUserAttrs: (trialId: number, user_attrs: {
        [key: string]: number | string;
    }) => Promise<void>;
    getParamImportances: (studyId: number) => Promise<ParamImportance[][]>;
    reportPreference: (studyId: number, candidates: number[], clicked: number) => Promise<void>;
    skipPreferentialTrial: (studyId: number, trialId: number) => Promise<void>;
    removePreferentialHistory: (studyId: number, historyUuid: string) => Promise<void>;
    restorePreferentialHistory: (studyId: number, historyUuid: string) => Promise<void>;
    reportFeedbackComponent: (studyId: number, component_type: FeedbackComponentType) => Promise<void>;
    getPlot: (studyId: number, plotType: PlotType) => Promise<PlotResponse>;
    getCompareStudiesPlot: (studyIds: number[], plotType: CompareStudiesPlotType) => Promise<PlotResponse>;
}
