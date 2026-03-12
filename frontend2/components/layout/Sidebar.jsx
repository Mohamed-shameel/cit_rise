'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { logout } from '../../lib/auth'

const navItems = [
  { label: 'Dashboard',      icon: '📊', href: '/dashboard/student' },
  { label: 'Career Roadmap', icon: '🗺️', href: '/dashboard/student/career-roadmap' },
  { label: 'Network',        icon: '🔗', href: '/dashboard/student/network' },
  { label: 'Events',         icon: '📅', href: '/dashboard/student/events' },
]

export default function Sidebar() {
  const pathname = usePathname()
  const router = useRouter()

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  return (
    <aside className="w-56 h-screen sticky top-0 bg-white border-r border-gray-200 flex flex-col pt-4 pb-4 px-3 overflow-y-auto flex-shrink-0">
      {/* Nav items */}
      <nav className="flex flex-col gap-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white font-semibold'
                  : 'text-gray-600 hover:bg-blue-50 hover:text-blue-600'
              }`}
            >
              <span className="text-base">{item.icon}</span>
              {item.label}
            </Link>
          )
        })}
      </nav>

      {/* Submit Idea card */}
      <div className="mt-6 bg-white border border-gray-200 rounded-xl p-4">
        <div className="flex flex-col items-center">
          <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 text-xl">
            💡
          </div>
          <p className="font-semibold text-sm text-gray-900 mt-2 text-center">Submit Your Idea</p>
          <p className="text-xs text-gray-500 text-center mt-1">
            Have a breakthrough? Share your innovative ideas with the CIT community and get them noticed.
          </p>
          <button
            onClick={() => router.push('/dashboard/student')}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold py-2 rounded-lg mt-3 transition-colors"
          >
            Submit Idea
          </button>
        </div>
      </div>

      {/* User section */}
      <div className="mt-auto pt-4 border-t border-gray-200">
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
            A
          </div>
          <div className="min-w-0">
            <p className="text-sm font-semibold text-gray-900 truncate">Ananya Sharma</p>
            <button
              onClick={handleLogout}
              className="text-xs text-gray-500 flex items-center gap-1 hover:text-red-500 transition-colors"
            >
              <span>↩</span> Sign Out
            </button>
          </div>
        </div>
      </div>
    </aside>
  )
}
