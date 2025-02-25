import React from "react";
import { APIClient } from "./apiClient";
type APIClientContextType = {
    apiClient: APIClient;
};
export declare const APIClientContext: React.Context<APIClientContextType | undefined>;
export declare const useAPIClient: () => APIClientContextType;
export declare function APIClientProvider({ apiClient, children, }: {
    apiClient: APIClient;
    children: React.ReactNode;
}): React.JSX.Element;
export {};
