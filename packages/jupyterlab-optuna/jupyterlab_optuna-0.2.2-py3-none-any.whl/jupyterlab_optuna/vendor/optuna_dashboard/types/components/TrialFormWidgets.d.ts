import * as Optuna from "@optuna/types";
import { FC, ReactNode } from "react";
import { FormWidgets, ObjectiveChoiceWidget, ObjectiveSliderWidget, ObjectiveTextInputWidget, ObjectiveUserAttrRef, Trial } from "ts/types/optuna";
type WidgetState = {
    isValid: boolean;
    value: number | string;
    render: () => ReactNode;
};
export declare const TrialFormWidgets: FC<{
    trial: Trial;
    objectiveNames: string[];
    directions: Optuna.StudyDirection[];
    formWidgets?: FormWidgets;
}>;
export declare const useTextInputWidget: (key: string, widgetType: "user_attr" | "objective", widget: ObjectiveTextInputWidget, metricName: string) => WidgetState;
export declare const useChoiceWidget: (key: string, widgetType: "user_attr" | "objective", widget: ObjectiveChoiceWidget, metricName: string) => WidgetState;
export declare const useSliderWidget: (key: string, widgetType: "user_attr" | "objective", widget: ObjectiveSliderWidget, metricName: string) => WidgetState;
export declare const useUserAttrRefWidget: (key: string, widget: ObjectiveUserAttrRef, metricName: string, trial: Trial) => WidgetState;
export {};
