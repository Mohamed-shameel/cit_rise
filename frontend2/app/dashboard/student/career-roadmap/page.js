'use client'

import TopNavbar from '../../../../components/layout/TopNavbar'
import Sidebar from '../../../../components/layout/Sidebar'

export default function CareerRoadmapPage() {
  return (
    <div className="flex flex-col h-screen">
      <TopNavbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-6 bg-gray-100">
          <h1 className="text-2xl font-bold text-gray-900">Career Roadmap</h1>
          <p className="text-gray-500 mt-2">Track your professional growth and plan your career path.</p>

          {/* Roadmap placeholder */}
          <div className="mt-8 grid grid-cols-3 gap-6">
            {[
              { stage: '1', title: 'Foundation', status: 'Completed', color: 'bg-green-500', items: ['Python Basics', 'Data Structures', 'Git & GitHub'] },
              { stage: '2', title: 'Core Skills', status: 'In Progress', color: 'bg-blue-500', items: ['Machine Learning', 'Web Development', 'System Design'] },
              { stage: '3', title: 'Advanced', status: 'Upcoming', color: 'bg-gray-300', items: ['Deep Learning', 'Cloud Platforms', 'Open Source'] },
            ].map((phase) => (
              <div key={phase.stage} className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
                <div className="flex items-center gap-3 mb-4">
                  <div className={`w-9 h-9 rounded-full flex items-center justify-center text-white font-bold ${phase.color}`}>
                    {phase.stage}
                  </div>
                  <div>
                    <p className="font-bold text-gray-900 text-sm">{phase.title}</p>
                    <span className={`text-[10px] font-semibold uppercase ${phase.status === 'Completed' ? 'text-green-600' : phase.status === 'In Progress' ? 'text-blue-600' : 'text-gray-400'}`}>
                      {phase.status}
                    </span>
                  </div>
                </div>
                <ul className="flex flex-col gap-2">
                  {phase.items.map((item) => (
                    <li key={item} className="flex items-center gap-2 text-sm text-gray-700">
                      <span className={`w-2 h-2 rounded-full flex-shrink-0 ${phase.color}`} />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  )
}
