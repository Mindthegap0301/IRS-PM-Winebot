import dayjs from "dayjs";
var isToday = require("dayjs/plugin/isToday");

dayjs.extend(isToday);

export const displayTime = (dateTime) => {
  if (dateTime) {
    const d = dayjs(dateTime);
    if (d.isToday()) {
      return d.format("h:mm A");
    } else {
      return d.format("h:mm A D MMM, YYYY");
    }
  }
  return null;
};
