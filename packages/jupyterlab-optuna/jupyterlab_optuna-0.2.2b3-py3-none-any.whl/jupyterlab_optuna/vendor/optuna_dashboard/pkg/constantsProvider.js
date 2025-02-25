import React from "react";
export const ConstantsContext = React.createContext({
    environment: "optuna-dashboard",
    url_prefix: "",
});
export const useConstants = () => {
    return React.useContext(ConstantsContext);
};
//# sourceMappingURL=constantsProvider.js.map