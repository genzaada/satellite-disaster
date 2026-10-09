/**
 * Backend health check response contract.
 */
export interface HealthResponse {
  status: string;
  version: string;
  environment: string;
  timestamp: string;
}
