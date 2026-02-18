import { useEffect, useState } from "react"
import { Link, useLocation } from "react-router-dom"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Sheet, SheetContent, SheetTrigger, SheetTitle } from "@/components/ui/sheet"
import { ThemeToggle } from "@/components/theme-toggle"
import type { ResolutionResponse, DueReminder } from "@/api/types"
import { listResolutions } from "@/api/client"

interface SidebarProps {
  reminders: DueReminder[]
}

function SidebarContent({ reminders }: SidebarProps) {
  const [resolutions, setResolutions] = useState<ResolutionResponse[]>([])
  const location = useLocation()

  useEffect(() => {
    listResolutions().then(setResolutions).catch(() => {})
  }, [location.pathname])

  const overdueIds = new Set(reminders.map((r) => r.resolution_id))

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between px-4 py-3">
        <Link to="/" className="text-lg font-semibold">
          Resolutions
        </Link>
        <ThemeToggle />
      </div>
      <Separator />
      <nav className="flex-1 overflow-y-auto px-2 py-2">
        <Link to="/">
          <Button
            variant={location.pathname === "/" ? "secondary" : "ghost"}
            className="w-full justify-start mb-1"
          >
            Dashboard
          </Button>
        </Link>
        <Separator className="my-2" />
        <p className="px-2 py-1 text-xs font-medium text-muted-foreground">
          My Resolutions
        </p>
        {resolutions.map((r) => (
          <Link key={r.id} to={`/resolution/${r.id}`}>
            <Button
              variant={
                location.pathname === `/resolution/${r.id}`
                  ? "secondary"
                  : "ghost"
              }
              className="w-full justify-start mb-0.5 text-sm"
            >
              <span className="truncate flex-1 text-left">{r.title}</span>
              {overdueIds.has(r.id) && (
                <Badge variant="destructive" className="ml-2 text-xs">
                  Due
                </Badge>
              )}
            </Button>
          </Link>
        ))}
        {resolutions.length === 0 && (
          <p className="px-2 py-4 text-sm text-muted-foreground">
            No resolutions yet
          </p>
        )}
      </nav>
    </div>
  )
}

export function Sidebar({ reminders }: SidebarProps) {
  return (
    <>
      {/* Desktop sidebar */}
      <aside className="hidden md:flex md:w-64 md:flex-col md:border-r bg-card">
        <SidebarContent reminders={reminders} />
      </aside>

      {/* Mobile sidebar */}
      <div className="md:hidden fixed top-3 left-3 z-40">
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="outline" size="icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-64 p-0">
            <SheetTitle className="sr-only">Navigation</SheetTitle>
            <SidebarContent reminders={reminders} />
          </SheetContent>
        </Sheet>
      </div>
    </>
  )
}
