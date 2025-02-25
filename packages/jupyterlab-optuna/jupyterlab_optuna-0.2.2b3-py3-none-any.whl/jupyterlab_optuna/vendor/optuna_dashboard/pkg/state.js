import { atom, useRecoilValue } from "recoil";
import { useLocalStorage } from "usehooks-ts";
import { DarkColorTemplates, LightColorTemplates, } from "./components/PlotlyColorTemplates";
export const studySummariesState = atom({
    key: "studySummaries",
    default: [],
});
export const studyDetailsState = atom({
    key: "studyDetails",
    default: {},
});
export const trialsUpdatingState = atom({
    key: "trialsUpdating",
    default: {},
});
// TODO(c-bata): Consider representing the state as boolean.
export const reloadIntervalState = atom({
    key: "reloadInterval",
    default: 10,
});
export const drawerOpenState = atom({
    key: "drawerOpen",
    default: false,
});
export const isFileUploading = atom({
    key: "isFileUploading",
    default: false,
});
export const artifactIsAvailable = atom({
    key: "artifactIsAvailable",
    default: false,
});
export const plotlypyIsAvailableState = atom({
    key: "plotlypyIsAvailable",
    default: false,
});
export const studySummariesLoadingState = atom({
    key: "studySummariesLoadingState",
    default: false,
});
export const studyDetailLoadingState = atom({
    key: "studyDetailLoading",
    default: {},
});
export const usePlotBackendRendering = () => {
    return useLocalStorage("plotBackendRendering", false);
};
export const useShowExperimentalFeature = () => {
    return useLocalStorage("showExperimentalFeature", false);
};
export const usePlotlyColorThemeState = () => {
    return useLocalStorage("plotlyColorTheme", {
        dark: "default",
        light: "default",
    });
};
export const useStudyDetailValue = (studyId) => {
    const studyDetails = useRecoilValue(studyDetailsState);
    return studyDetails[studyId] || null;
};
export const useStudySummaryValue = (studyId) => {
    const studySummaries = useRecoilValue(studySummariesState);
    return studySummaries.find((s) => s.study_id === studyId) || null;
};
export const useTrialUpdatingValue = (trialId) => {
    const updating = useRecoilValue(trialsUpdatingState);
    return updating[trialId] || false;
};
export const useStudyDirections = (studyId) => {
    const studyDetail = useStudyDetailValue(studyId);
    const studySummary = useStudySummaryValue(studyId);
    return (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.directions) || (studySummary === null || studySummary === void 0 ? void 0 : studySummary.directions) || null;
};
export const useStudyIsPreferential = (studyId) => {
    const studyDetail = useStudyDetailValue(studyId);
    const studySummary = useStudySummaryValue(studyId);
    return (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.is_preferential) || (studySummary === null || studySummary === void 0 ? void 0 : studySummary.is_preferential) || null;
};
export const useStudyName = (studyId) => {
    const studyDetail = useStudyDetailValue(studyId);
    const studySummary = useStudySummaryValue(studyId);
    return (studyDetail === null || studyDetail === void 0 ? void 0 : studyDetail.name) || (studySummary === null || studySummary === void 0 ? void 0 : studySummary.study_name) || null;
};
export const useArtifacts = (studyId, trialId) => {
    const study = useStudyDetailValue(studyId);
    const trial = study === null || study === void 0 ? void 0 : study.trials.find((t) => t.trial_id === trialId);
    if (trial === undefined) {
        return [];
    }
    return trial.artifacts;
};
export const usePlotlyColorTheme = (mode) => {
    const [theme] = usePlotlyColorThemeState();
    if (mode === "dark") {
        return DarkColorTemplates[theme.dark];
    }
    else {
        return LightColorTemplates[theme.light];
    }
};
export const useBackendRender = () => {
    const [plotBackendRendering] = usePlotBackendRendering();
    const plotlypyIsAvailable = useRecoilValue(plotlypyIsAvailableState);
    if (plotBackendRendering) {
        if (plotlypyIsAvailable) {
            return true;
        }
    }
    return false;
};
//# sourceMappingURL=state.js.map