export const formatDate = (date) => {
    const options = {
        year: "numeric",
        month: "numeric",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
    };
    return new Intl.DateTimeFormat("ja-JP", options).format(date);
};
//# sourceMappingURL=dateUtil.js.map