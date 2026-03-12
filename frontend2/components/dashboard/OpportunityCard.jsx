'use client'

const badgeStyles = {
  HACKATHON:    'bg-blue-50 text-blue-600 border border-blue-200',
  'OPEN SOURCE':'bg-green-50 text-green-600 border border-green-200',
  INTERNSHIP:   'bg-yellow-50 text-yellow-600 border border-yellow-200',
  COMPETITION:  'bg-purple-50 text-purple-600 border border-purple-200',
}

export default function OpportunityCard({ type, title, organizer, deadline, location, buttonLabel }) {
  const badge = badgeStyles[type] || 'bg-gray-100 text-gray-600 border border-gray-200'

  return (
    <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 flex flex-col h-full">
      {/* Top row */}
      <div className="flex justify-between items-start">
        <span className={`text-[10px] font-bold uppercase px-2 py-1 rounded-full ${badge}`}>
          {type}
        </span>
        <button className="text-gray-400 text-sm cursor-pointer hover:text-gray-600">🔖</button>
      </div>

      {/* Title & organizer */}
      <p className="font-bold text-gray-900 text-base mt-3 leading-snug">{title}</p>
      <p className="text-gray-500 text-sm mt-1">{organizer}</p>

      {/* Details */}
      <div className="mt-3 flex flex-col gap-1.5">
        <div className="flex items-center gap-1.5">
          <span className="text-gray-400 text-xs">📅</span>
          <span className="text-gray-500 text-xs">Deadline: {deadline}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-gray-400 text-xs">📍</span>
          <span className="text-gray-500 text-xs">{location}</span>
        </div>
      </div>

      {/* CTA */}
      <button className="mt-auto pt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm py-2.5 rounded-lg transition-colors">
        {buttonLabel}
      </button>
    </div>
  )
}
