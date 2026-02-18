import type {
  ResolutionCreate,
  ResolutionUpdate,
  ResolutionResponse,
  ResolutionDetail,
  CheckInCreate,
  CheckInResponse,
  ReminderUpdate,
  ReminderResponse,
  DueReminder,
  DashboardSummary,
} from "./types"

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  })
  if (!res.ok) {
    const body = await res.text().catch(() => "")
    throw new Error(`${res.status}: ${body}`)
  }
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}

export async function listResolutions(): Promise<ResolutionResponse[]> {
  return request<ResolutionResponse[]>("/api/resolutions")
}

export async function createResolution(data: ResolutionCreate): Promise<ResolutionResponse> {
  return request<ResolutionResponse>("/api/resolutions", {
    method: "POST",
    body: JSON.stringify(data),
  })
}

export async function getResolution(id: number): Promise<ResolutionDetail> {
  return request<ResolutionDetail>(`/api/resolutions/${id}`)
}

export async function updateResolution(id: number, data: ResolutionUpdate): Promise<ResolutionResponse> {
  return request<ResolutionResponse>(`/api/resolutions/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  })
}

export async function deleteResolution(id: number): Promise<void> {
  return request<void>(`/api/resolutions/${id}`, { method: "DELETE" })
}

export async function listCheckIns(resolutionId: number): Promise<CheckInResponse[]> {
  return request<CheckInResponse[]>(`/api/resolutions/${resolutionId}/check-ins`)
}

export async function createCheckIn(resolutionId: number, data: CheckInCreate): Promise<CheckInResponse> {
  return request<CheckInResponse>(`/api/resolutions/${resolutionId}/check-ins`, {
    method: "POST",
    body: JSON.stringify(data),
  })
}

export async function getDueReminders(): Promise<DueReminder[]> {
  return request<DueReminder[]>("/api/reminders/due")
}

export async function updateReminder(resolutionId: number, data: ReminderUpdate): Promise<ReminderResponse> {
  return request<ReminderResponse>(`/api/resolutions/${resolutionId}/reminder`, {
    method: "PUT",
    body: JSON.stringify(data),
  })
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  return request<DashboardSummary>("/api/dashboard/summary")
}
