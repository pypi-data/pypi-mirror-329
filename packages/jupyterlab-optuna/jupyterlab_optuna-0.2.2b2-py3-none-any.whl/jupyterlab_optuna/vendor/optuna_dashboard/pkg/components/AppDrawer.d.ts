import React, { FC } from "react";
export type PageId = "top" | "analytics" | "trialTable" | "trialList" | "trialSelection" | "note" | "preferenceHistory" | "graph";
export declare const AppDrawer: FC<{
    studyId?: number;
    toggleColorMode: () => void;
    page?: PageId;
    toolbar: React.ReactNode;
    children?: React.ReactNode;
}>;
