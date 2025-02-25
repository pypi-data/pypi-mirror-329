const filterFunc = (trial, directions) => {
    return (trial.state === "Complete" &&
        trial.values !== undefined &&
        trial.values.length === directions.length);
};
export const getDominatedTrials = (trials, directions) => {
    // TODO(c-bata): Use log-linear algorithm like Optuna.
    // TODO(c-bata): Use this function at GraphParetoFront.
    const filteredTrials = trials.filter((t) => filterFunc(t, directions));
    const normalizedValues = [];
    filteredTrials.forEach((t) => {
        if (t.values && t.values.length === directions.length) {
            const trialValues = t.values.map((v, i) => {
                return directions[i] === "minimize" ? v : -v;
            });
            normalizedValues.push(trialValues);
        }
    });
    const dominatedTrials = [];
    normalizedValues.forEach((values0, i) => {
        const dominated = normalizedValues.some((values1, j) => {
            if (i === j || values0.every((v, i) => v === values1[i])) {
                return false;
            }
            return values0.every((value0, k) => {
                return values1[k] <= value0;
            });
        });
        dominatedTrials.push(dominated);
    });
    return filteredTrials.filter((_, i) => !dominatedTrials.at(i));
};
//# sourceMappingURL=dominatedTrials.js.map