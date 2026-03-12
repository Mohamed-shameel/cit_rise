'use client'

import TopNavbar from '../../../components/layout/TopNavbar'
import Sidebar from '../../../components/layout/Sidebar'

export default function ClubDashboard() {
  return (
    <div className="flex flex-col h-screen">
      <TopNavbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-6 bg-gray-100 flex items-center justify-center">
          <div className="text-center">
            <div className="text-5xl mb-4">🏛️</div>
            <h1 className="text-2xl font-bold text-gray-900">Club Dashboard</h1>
            <p className="text-gray-500 mt-2">Welcome, Club Representative. Dashboard coming soon.</p>
          </div>
        </main>
      </div>
    </div>
  )
}
