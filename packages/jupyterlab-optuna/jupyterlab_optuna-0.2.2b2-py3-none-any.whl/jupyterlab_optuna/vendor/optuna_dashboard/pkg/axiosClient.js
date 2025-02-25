import axios from "axios";
import { APIClient, } from "./apiClient";
export class AxiosClient extends APIClient {
    constructor(API_ENDPOINT) {
        super();
        this.getMetaInfo = () => this.axiosInstance
            .get(`/api/meta`)
            .then((res) => res.data);
        this.getStudyDetail = (studyId, nLocalTrials) => this.axiosInstance
            .get(`/api/studies/${studyId}`, {
            params: {
                after: nLocalTrials,
            },
        })
            .then((res) => {
            var _a, _b;
            const trials = res.data.trials.map((trial) => {
                return this.convertTrialResponse(trial);
            });
            const best_trials = res.data.best_trials.map((trial) => {
                return this.convertTrialResponse(trial);
            });
            return {
                id: studyId,
                name: res.data.name,
                datetime_start: new Date(res.data.datetime_start),
                directions: res.data.directions,
                user_attrs: res.data.user_attrs,
                trials: trials,
                best_trials: best_trials,
                union_search_space: res.data.union_search_space,
                intersection_search_space: res.data.intersection_search_space,
                union_user_attrs: res.data.union_user_attrs,
                has_intermediate_values: res.data.has_intermediate_values,
                note: res.data.note,
                metric_names: res.data.objective_names,
                form_widgets: res.data.form_widgets,
                is_preferential: res.data.is_preferential,
                feedback_component_type: res.data.feedback_component_type,
                preferences: res.data.preferences,
                preference_history: (_a = res.data.preference_history) === null || _a === void 0 ? void 0 : _a.map(this.convertPreferenceHistory),
                plotly_graph_objects: res.data.plotly_graph_objects,
                artifacts: res.data.artifacts,
                skipped_trial_numbers: (_b = res.data.skipped_trial_numbers) !== null && _b !== void 0 ? _b : [],
            };
        });
        this.getStudySummaries = () => this.axiosInstance
            .get(`/api/studies`, {})
            .then((res) => {
            return res.data.study_summaries.map((study) => {
                return {
                    study_id: study.study_id,
                    study_name: study.study_name,
                    directions: study.directions,
                    user_attrs: study.user_attrs,
                    is_preferential: study.is_preferential,
                    datetime_start: study.datetime_start
                        ? new Date(study.datetime_start)
                        : undefined,
                };
            });
        });
        this.createNewStudy = (studyName, directions) => this.axiosInstance
            .post(`/api/studies`, {
            study_name: studyName,
            directions,
        })
            .then((res) => {
            const study_summary = res.data.study_summary;
            return {
                study_id: study_summary.study_id,
                study_name: study_summary.study_name,
                directions: study_summary.directions,
                // best_trial: undefined,
                user_attrs: study_summary.user_attrs,
                is_preferential: study_summary.is_preferential,
                datetime_start: study_summary.datetime_start
                    ? new Date(study_summary.datetime_start)
                    : undefined,
            };
        });
        this.deleteStudy = (studyId, removeAssociatedArtifacts) => this.axiosInstance
            .delete(`/api/studies/${studyId}`, {
            data: {
                remove_associated_artifacts: removeAssociatedArtifacts,
            },
        })
            .then(() => {
            return;
        });
        this.renameStudy = (studyId, studyName) => this.axiosInstance
            .post(`/api/studies/${studyId}/rename`, {
            study_name: studyName,
        })
            .then((res) => {
            return {
                study_id: res.data.study_id,
                study_name: res.data.study_name,
                directions: res.data.directions,
                user_attrs: res.data.user_attrs,
                is_preferential: res.data.is_prefential,
                datetime_start: res.data.datetime_start
                    ? new Date(res.data.datetime_start)
                    : undefined,
            };
        });
        this.saveStudyNote = (studyId, note) => this.axiosInstance
            .put(`/api/studies/${studyId}/note`, note)
            .then(() => {
            return;
        });
        this.saveTrialNote = (studyId, trialId, note) => this.axiosInstance
            .put(`/api/studies/${studyId}/${trialId}/note`, note)
            .then(() => {
            return;
        });
        this.uploadTrialArtifact = (studyId, trialId, fileName, dataUrl) => this.axiosInstance
            .post(`/api/artifacts/${studyId}/${trialId}`, {
            file: dataUrl,
            filename: fileName,
        })
            .then((res) => {
            return res.data;
        });
        this.uploadStudyArtifact = (studyId, fileName, dataUrl) => this.axiosInstance
            .post(`/api/artifacts/${studyId}`, {
            file: dataUrl,
            filename: fileName,
        })
            .then((res) => {
            return res.data;
        });
        this.deleteTrialArtifact = (studyId, trialId, artifactId) => this.axiosInstance
            .delete(`/api/artifacts/${studyId}/${trialId}/${artifactId}`)
            .then(() => {
            return;
        });
        this.deleteStudyArtifact = (studyId, artifactId) => this.axiosInstance
            .delete(`/api/artifacts/${studyId}/${artifactId}`)
            .then(() => {
            return;
        });
        this.tellTrial = (trialId, state, values) => this.axiosInstance
            .post(`/api/trials/${trialId}/tell`, {
            state,
            values,
        })
            .then(() => {
            return;
        });
        this.saveTrialUserAttrs = (trialId, user_attrs) => this.axiosInstance
            .post(`/api/trials/${trialId}/user-attrs`, { user_attrs })
            .then(() => {
            return;
        });
        this.getParamImportances = (studyId) => this.axiosInstance
            .get(`/api/studies/${studyId}/param_importances`)
            .then((res) => {
            return res.data.param_importances;
        });
        this.reportPreference = (studyId, candidates, clicked) => this.axiosInstance
            .post(`/api/studies/${studyId}/preference`, {
            candidates: candidates,
            clicked: clicked,
            mode: "ChooseWorst",
        })
            .then(() => {
            return;
        });
        this.skipPreferentialTrial = (studyId, trialId) => this.axiosInstance
            .post(`/api/studies/${studyId}/${trialId}/skip`)
            .then(() => {
            return;
        });
        this.removePreferentialHistory = (studyId, historyUuid) => this.axiosInstance
            .delete(`/api/studies/${studyId}/preference/${historyUuid}`)
            .then(() => {
            return;
        });
        this.restorePreferentialHistory = (studyId, historyUuid) => this.axiosInstance
            .post(`/api/studies/${studyId}/preference/${historyUuid}`)
            .then(() => {
            return;
        });
        this.reportFeedbackComponent = (studyId, component_type) => this.axiosInstance
            .put(`/api/studies/${studyId}/preference_feedback_component`, component_type)
            .then(() => {
            return;
        });
        this.getPlot = (studyId, plotType) => this.axiosInstance
            .get(`/api/studies/${studyId}/plot/${plotType}`)
            .then((res) => res.data);
        this.getCompareStudiesPlot = (studyIds, plotType) => this.axiosInstance
            .get(`/api/compare-studies/plot/${plotType}`, {
            params: { study_ids: studyIds },
        })
            .then((res) => res.data);
        this.axiosInstance = axios.create({ baseURL: API_ENDPOINT });
    }
}
//# sourceMappingURL=axiosClient.js.map