'use client'

import { useRouter } from 'next/navigation'

const deadlines = [
  { title: 'Project Proposal Submission', sub: 'Due in 2 days • Oct 20', color: 'bg-red-500' },
  { title: 'ML Hackathon Registration',   sub: 'Due in 5 days • Oct 23', color: 'bg-orange-400' },
  { title: 'GSoc Mentorship Call',        sub: 'Scheduled • Oct 28',     color: 'bg-blue-500' },
]

const mentors = [
  { name: 'Dr. Emily Watson',  domain: 'Data Science & Ethics', initials: 'E', color: 'bg-rose-500' },
  { name: 'Mark J. Peterson',  domain: 'Software Engineering',  initials: 'M', color: 'bg-indigo-500' },
  { name: 'Julian Thorne',     domain: 'Startup Mentorship',    initials: 'J', color: 'bg-emerald-500' },
]

export default function RightPanel() {
  const router = useRouter()

  return (
    <aside className="w-72 h-screen sticky top-16 overflow-y-auto p-4 flex flex-col gap-4 flex-shrink-0">
      {/* Upcoming Deadlines */}
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <div className="flex items-center gap-2">
          <span className="text-base">🔴</span>
          <span className="font-semibold text-gray-900 text-sm">Upcoming Deadlines</span>
        </div>
        <div className="mt-3 flex flex-col gap-3">
          {deadlines.map((d) => (
            <div key={d.title} className="flex items-start gap-3">
              <div className={`w-1 min-h-8 rounded-full flex-shrink-0 mt-0.5 ${d.color}`} />
              <div>
                <p className="text-sm font-semibold text-gray-900 leading-snug">{d.title}</p>
                <p className="text-xs text-gray-500 mt-0.5">{d.sub}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Suggested Mentors */}
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <p className="font-semibold text-gray-900 text-sm">Suggested Mentors</p>
        <div className="mt-3 flex flex-col gap-3">
          {mentors.map((m) => (
            <div key={m.name} className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className={`w-9 h-9 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0 ${m.color}`}>
                  {m.initials}
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900">{m.name}</p>
                  <p className="text-xs text-gray-500">{m.domain}</p>
                </div>
              </div>
              <button className="w-7 h-7 bg-blue-50 rounded-full flex items-center justify-center text-blue-600 hover:bg-blue-100 text-sm">
                ➕
              </button>
            </div>
          ))}
        </div>
        <button
          onClick={() => router.push('/dashboard/student/network')}
          className="w-full text-blue-600 text-xs font-medium text-center mt-3 hover:underline cursor-pointer"
        >
          View All Mentors
        </button>
      </div>

      {/* Build Your Network */}
      <div className="rounded-xl p-5" style={{ background: 'linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%)' }}>
        <p className="font-bold text-white text-base">Build Your Network</p>
        <p className="text-blue-100 text-xs mt-1">Connect with 500+ alumni from top tech companies.</p>
        <button
          onClick={() => router.push('/dashboard/student/network')}
          className="bg-white text-blue-700 font-semibold text-xs rounded-full px-4 py-1.5 mt-4 inline-block hover:bg-blue-50 transition-colors"
        >
          Get Started
        </button>
      </div>
    </aside>
  )
}
