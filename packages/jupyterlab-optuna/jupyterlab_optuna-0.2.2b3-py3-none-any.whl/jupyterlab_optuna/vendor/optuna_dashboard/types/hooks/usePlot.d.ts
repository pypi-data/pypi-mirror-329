import { AxiosError } from "axios";
import * as plotly from "plotly.js-dist-min";
import { PlotType } from "../apiClient";
export declare const usePlot: ({ numCompletedTrials, studyId, plotType, }: {
    numCompletedTrials: number;
    studyId: number | undefined;
    plotType: PlotType;
}) => {
    data: plotly.Data[] | undefined;
    layout: plotly.Layout | undefined;
    isLoading: boolean;
    error: AxiosError<unknown, any> | null;
};
