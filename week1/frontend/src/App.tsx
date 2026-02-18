import { Routes, Route } from "react-router-dom"
import { Sidebar } from "@/components/sidebar"
import { ReminderBanner } from "@/components/reminder-banner"
import { useReminders } from "@/hooks/use-reminders"
import { Dashboard } from "@/pages/dashboard"
import { ResolutionDetail } from "@/pages/resolution-detail"

export default function App() {
  const { reminders } = useReminders()

  return (
    <div className="flex h-screen">
      <Sidebar reminders={reminders} />
      <main className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-4xl px-4 py-6 md:px-8 space-y-6">
          <ReminderBanner reminders={reminders} />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/resolution/:id" element={<ResolutionDetail />} />
          </Routes>
        </div>
      </main>
    </div>
  )
}
