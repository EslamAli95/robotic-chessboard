// src/reportWebVitals.ts
import { ReportHandler } from "web-vitals";

/**
 * Log performance metrics or send to an analytics endpoint.
 * @param onPerfEntry - callback to handle a single metric.
 */
const reportWebVitals = (onPerfEntry?: ReportHandler): void => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import("web-vitals")
      .then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
        getCLS(onPerfEntry);
        getFID(onPerfEntry);
        getFCP(onPerfEntry);
        getLCP(onPerfEntry);
        getTTFB(onPerfEntry);
      })
      .catch((err) => console.error("Error importing web-vitals", err));
  }
};

export default reportWebVitals;
