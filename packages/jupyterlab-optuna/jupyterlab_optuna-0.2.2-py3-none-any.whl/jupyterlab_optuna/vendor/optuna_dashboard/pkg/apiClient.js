export var PlotType;
(function (PlotType) {
    PlotType["Contour"] = "contour";
    PlotType["Slice"] = "slice";
    PlotType["ParallelCoordinate"] = "parallel_coordinate";
    PlotType["Rank"] = "rank";
    PlotType["EDF"] = "edf";
    PlotType["Timeline"] = "timeline";
    PlotType["ParamImportances"] = "param_importances";
    PlotType["ParetoFront"] = "pareto_front";
})(PlotType || (PlotType = {}));
export var CompareStudiesPlotType;
(function (CompareStudiesPlotType) {
    CompareStudiesPlotType["EDF"] = "edf";
})(CompareStudiesPlotType || (CompareStudiesPlotType = {}));
export class APIClient {
    constructor() { }
    convertTrialResponse(response) {
        return {
            trial_id: response.trial_id,
            study_id: response.study_id,
            number: response.number,
            state: response.state,
            values: response.values,
            intermediate_values: response.intermediate_values,
            datetime_start: response.datetime_start
                ? new Date(response.datetime_start)
                : undefined,
            datetime_complete: response.datetime_complete
                ? new Date(response.datetime_complete)
                : undefined,
            params: response.params,
            fixed_params: response.fixed_params,
            user_attrs: response.user_attrs,
            note: response.note,
            artifacts: response.artifacts,
            constraints: response.constraints,
        };
    }
    convertPreferenceHistory(response) {
        return {
            id: response.history.id,
            candidates: response.history.candidates,
            clicked: response.history.clicked,
            feedback_mode: response.history.mode,
            timestamp: new Date(response.history.timestamp),
            preferences: response.history.preferences,
            is_removed: response.is_removed,
        };
    }
}
//# sourceMappingURL=apiClient.js.map