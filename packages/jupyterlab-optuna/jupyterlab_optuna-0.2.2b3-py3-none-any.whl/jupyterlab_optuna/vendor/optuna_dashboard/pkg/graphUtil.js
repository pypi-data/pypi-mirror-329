const PADDING_RATIO = 0.05;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const unique = (array) => {
    const knownElements = new Map();
    array.forEach((elem) => knownElements.set(elem, true));
    return Array.from(knownElements.keys());
};
export const getAxisInfo = (trials, param) => {
    if (param.distribution.type === "CategoricalDistribution") {
        return getAxisInfoForCategoricalParams(trials, param.name, param.distribution);
    }
    else {
        return getAxisInfoForNumericalParams(trials, param.name, param.distribution);
    }
};
const getAxisInfoForCategoricalParams = (trials, paramName, distribution) => {
    const values = trials.map((trial) => {
        var _a;
        return ((_a = trial.params.find((p) => p.name === paramName)) === null || _a === void 0 ? void 0 : _a.param_external_value) ||
            null;
    });
    const indices = distribution.choices
        .map((c) => { var _a; return (_a = c === null || c === void 0 ? void 0 : c.value) !== null && _a !== void 0 ? _a : "null"; })
        .sort((a, b) => a.toLowerCase() < b.toLowerCase()
        ? -1
        : a.toLowerCase() > b.toLowerCase()
            ? 1
            : 0);
    return {
        name: paramName,
        isLog: false,
        isCat: true,
        indices,
        values,
    };
};
const getAxisInfoForNumericalParams = (trials, paramName, distribution) => {
    let min = 0;
    let max = 0;
    if (distribution.log) {
        const padding = (Math.log10(distribution.high) - Math.log10(distribution.low)) *
            PADDING_RATIO;
        min = Math.pow(10, Math.log10(distribution.low) - padding);
        max = Math.pow(10, Math.log10(distribution.high) + padding);
    }
    else {
        const padding = (distribution.high - distribution.low) * PADDING_RATIO;
        min = distribution.low - padding;
        max = distribution.high + padding;
    }
    const values = trials.map((trial) => {
        var _a;
        return ((_a = trial.params.find((p) => p.name === paramName)) === null || _a === void 0 ? void 0 : _a.param_internal_value) ||
            null;
    });
    const indices = unique(values)
        .filter((v) => v !== null)
        .sort((a, b) => a - b);
    if (indices.length >= 2) {
        indices.unshift(min);
        indices.push(max);
    }
    return {
        name: paramName,
        isLog: distribution.log,
        isCat: false,
        indices,
        values,
    };
};
export const makeHovertext = (trial) => {
    return JSON.stringify({
        number: trial.number,
        values: trial.values,
        params: trial.params
            .map((p) => [p.name, p.param_external_value])
            .reduce((obj, [key, value]) => (Object.assign(Object.assign({}, obj), { [key]: value })), {}),
    }, undefined, "  ").replace(/\n/g, "<br>");
};
export const studyDetailToStudy = (studyDetail) => {
    const study = studyDetail
        ? {
            id: studyDetail.id,
            name: studyDetail.name,
            directions: studyDetail.directions,
            union_search_space: studyDetail.union_search_space,
            intersection_search_space: studyDetail.intersection_search_space,
            union_user_attrs: studyDetail.union_user_attrs,
            datetime_start: studyDetail.datetime_start,
            trials: studyDetail.trials,
            metric_names: studyDetail.metric_names,
        }
        : null;
    return study;
};
//# sourceMappingURL=graphUtil.js.map