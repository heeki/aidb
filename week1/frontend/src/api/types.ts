export interface ResolutionCreate {
  title: string
  description: string
  target_date?: string | null
}

export interface ResolutionUpdate {
  title?: string | null
  description?: string | null
  target_date?: string | null
  status?: string | null
}

export interface ResolutionResponse {
  id: number
  title: string
  description: string
  category: string | null
  priority: number | null
  target_date: string | null
  status: string
  created_at: string
  updated_at: string
}

export interface CheckInCreate {
  note: string
}

export interface CheckInResponse {
  id: number
  resolution_id: number
  note: string
  sentiment: string | null
  sentiment_score: number | null
  ai_feedback: string | null
  created_at: string
}

export interface ResolutionDetail extends ResolutionResponse {
  check_ins: CheckInResponse[]
  reminder: ReminderResponse | null
}

export interface ReminderUpdate {
  frequency: string
  is_active?: boolean
}

export interface ReminderResponse {
  id: number
  resolution_id: number
  frequency: string
  next_due: string
  is_active: boolean
}

export interface DueReminder {
  resolution_id: number
  resolution_title: string
  frequency: string
  next_due: string
}

export interface DashboardSummary {
  total_resolutions: number
  active_resolutions: number
  completed_resolutions: number
  abandoned_resolutions: number
  total_check_ins: number
  average_sentiment_score: number | null
  overdue_reminders: number
  sentiment_breakdown: Record<string, number>
}
