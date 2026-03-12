'use client'

export default function EventCard({ image, category, title, hostedBy, date, time }) {
  return (
    <div className="bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100">
      {/* Image area */}
      <div className="relative h-44 w-full bg-gray-200">
        {image ? (
          <img src={image} alt={title} className="object-cover w-full h-full" />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-blue-600 to-indigo-700 text-white text-4xl">
            {category === 'WORKSHOP' ? '🧠' : '⚡'}
          </div>
        )}
        <span className="absolute bottom-2 left-2 bg-black/60 text-white text-[10px] font-bold uppercase px-2.5 py-1 rounded">
          {category}
        </span>
      </div>

      {/* Body */}
      <div className="p-4">
        <p className="font-bold text-gray-900 text-base">{title}</p>
        <p className="text-gray-500 text-sm mt-1">Hosted by {hostedBy}</p>
        <div className="flex justify-between items-center mt-3">
          <div>
            <span className="font-bold text-blue-600 text-sm block">{date}</span>
            <span className="text-gray-500 text-xs">{time}</span>
          </div>
          <button className="border border-gray-200 text-gray-600 text-xs px-4 py-1.5 rounded-lg hover:border-blue-400 hover:text-blue-600 transition-colors">
            View Details
          </button>
        </div>
      </div>
    </div>
  )
}
