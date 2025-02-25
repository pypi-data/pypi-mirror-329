import React, { createContext, useContext } from "react";
export const APIClientContext = createContext(undefined);
export const useAPIClient = () => {
    const context = useContext(APIClientContext);
    if (context === undefined) {
        throw new Error("useAPIClient must be used within a APIClientProvider.");
    }
    return context;
};
export function APIClientProvider({ apiClient, children, }) {
    return (React.createElement(APIClientContext.Provider, { value: { apiClient } }, children));
}
//# sourceMappingURL=apiClientProvider.js.map