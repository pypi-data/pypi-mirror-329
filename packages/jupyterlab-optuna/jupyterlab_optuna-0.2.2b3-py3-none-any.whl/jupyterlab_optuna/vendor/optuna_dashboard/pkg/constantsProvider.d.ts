import React from "react";
type ConstantsContextType = {
    environment: "jupyterlab" | "optuna-dashboard";
    url_prefix: string;
};
export declare const ConstantsContext: React.Context<ConstantsContextType>;
export declare const useConstants: () => ConstantsContextType;
export {};
