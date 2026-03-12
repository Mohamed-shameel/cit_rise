'use client'

const roleBadge = {
  Mentor:  'bg-yellow-50 text-yellow-700 border border-yellow-200',
  Student: 'bg-blue-50 text-blue-600 border border-blue-200',
  Alumni:  'bg-green-50 text-green-600 border border-green-200',
}

export default function PersonCard({ name, role, description, avatarInitial, avatarColor }) {
  const badge = roleBadge[role] || 'bg-gray-100 text-gray-600 border border-gray-200'

  return (
    <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className={`w-11 h-11 rounded-full flex items-center justify-center text-white font-bold text-base flex-shrink-0 ${avatarColor}`}>
          {avatarInitial}
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-semibold text-gray-900 text-sm">{name}</span>
            <span className={`text-[11px] px-2 py-0.5 rounded-full font-medium ${badge}`}>{role}</span>
          </div>
          <p className="text-gray-500 text-xs mt-0.5">{description}</p>
        </div>
      </div>
      <button className="border border-blue-500 text-blue-600 text-xs font-semibold px-4 py-1.5 rounded-full hover:bg-blue-600 hover:text-white transition-colors flex-shrink-0">
        Connect
      </button>
    </div>
  )
}
