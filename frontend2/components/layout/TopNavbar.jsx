'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { logout } from '../../lib/auth'

export default function TopNavbar() {
  const router = useRouter()
  const [showDropdown, setShowDropdown] = useState(false)
  const [search, setSearch] = useState('')

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-gray-200 h-[60px] flex items-center justify-between px-6 w-full">
      {/* Left: Logo */}
      <div className="flex items-center gap-2 flex-shrink-0">
        <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white text-lg">
          🎓
        </div>
        <span className="font-bold text-gray-900 text-lg">CIT RISE</span>
      </div>

      {/* Center: Search */}
      <div className="flex-1 max-w-md mx-8">
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔍</span>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search opportunities, events, people..."
            className="w-full bg-gray-100 rounded-full pl-9 pr-4 py-2 text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-300"
          />
        </div>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-4">
        <button className="text-gray-500 hover:text-gray-700 text-xl w-9 h-9 flex items-center justify-center rounded-full hover:bg-gray-100">
          🌙
        </button>
        <button className="text-gray-500 hover:text-gray-700 text-xl w-9 h-9 flex items-center justify-center rounded-full hover:bg-gray-100">
          💬
        </button>

        {/* Avatar with dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowDropdown(!showDropdown)}
            className="w-9 h-9 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm hover:bg-blue-700"
          >
            A
          </button>
          {showDropdown && (
            <div className="absolute right-0 top-11 bg-white border border-gray-200 rounded-xl shadow-lg py-1 w-44 z-50">
              <button
                className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50"
                onClick={() => setShowDropdown(false)}
              >
                View Profile
              </button>
              <button
                className="w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-red-50"
                onClick={handleLogout}
              >
                Sign Out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
