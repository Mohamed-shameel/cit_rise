'use client'

import TopNavbar from '../../../../components/layout/TopNavbar'
import Sidebar from '../../../../components/layout/Sidebar'
import PersonCard from '../../../../components/dashboard/PersonCard'

const people = [
  { name: 'Dr. Emily Watson',  role: 'Mentor',  description: 'Data Science & Ethics • 10 yrs experience',       avatarInitial: 'E', avatarColor: 'bg-rose-500' },
  { name: 'Mark J. Peterson',  role: 'Mentor',  description: 'Software Engineering • Ex-Google Tech Lead',       avatarInitial: 'M', avatarColor: 'bg-indigo-500' },
  { name: 'Julian Thorne',     role: 'Mentor',  description: 'Startup Mentorship • Founded 3 startups',          avatarInitial: 'J', avatarColor: 'bg-amber-500' },
  { name: 'Priya Nair',        role: 'Alumni',  description: 'SWE @ Google • CIT Batch of 2022',                 avatarInitial: 'P', avatarColor: 'bg-emerald-500' },
  { name: 'Rahul Verma',       role: 'Student', description: 'CSE AI • Year 3 • Interested in ML & Robotics',    avatarInitial: 'R', avatarColor: 'bg-blue-500' },
  { name: 'Sarah Chen',        role: 'Mentor',  description: 'Senior AI Researcher @ DeepTech • Alumni \'20',    avatarInitial: 'S', avatarColor: 'bg-purple-500' },
]

export default function NetworkPage() {
  return (
    <div className="flex flex-col h-screen">
      <TopNavbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-6 bg-gray-100">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Network</h1>
              <p className="text-gray-500 text-sm mt-1">Connect with mentors, peers, and alumni.</p>
            </div>
            <div className="flex gap-2">
              {['All', 'Mentors', 'Students', 'Alumni'].map((tab) => (
                <button key={tab} className="px-4 py-1.5 rounded-full text-sm font-medium border border-gray-200 text-gray-600 hover:bg-blue-50 hover:text-blue-600 hover:border-blue-300 transition-colors">
                  {tab}
                </button>
              ))}
            </div>
          </div>
          <div className="flex flex-col gap-3">
            {people.map((p) => (
              <PersonCard key={p.name} {...p} />
            ))}
          </div>
        </main>
      </div>
    </div>
  )
}
