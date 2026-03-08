// frontend/app/components/Sidebar.js
'use client'

const CATEGORIES = [
  { id: "general",    label: "All Topics",  icon: "🏠" },
  { id: "academics",  label: "Academics",   icon: "📚" },
  { id: "facilities", label: "Facilities",  icon: "🏢" },
  { id: "placements", label: "Placements",  icon: "💼" },
  { id: "clubs",      label: "Clubs",       icon: "🎭" },
  { id: "contacts",   label: "Contacts",    icon: "📞" },
  { id: "locations",  label: "Locations",   icon: "🗺️" },
]

export default function Sidebar({ activeCategory, onCategoryChange }) {
  return (
    <div className="w-64 bg-gray-900 border-r border-gray-700 flex flex-col">

      
      {/* Categories */}
      <div className="p-4 flex-1">
        <p className="text-gray-500 text-xs uppercase mb-3">Filter by Category</p>
        {CATEGORIES.map(cat => (
          <button
            key={cat.id}
            onClick={() => onCategoryChange(cat.id)}
            className={`w-full text-left px-3 py-2 rounded-lg mb-1 flex items-center gap-2 transition-colors ${
              activeCategory === cat.id
                ? "bg-blue-600 text-white"
                : "text-gray-300 hover:bg-gray-800"
            }`}
          >
            <span>{cat.icon}</span>
            <span className="text-sm">{cat.label}</span>
          </button>
        ))}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-700">
        <p className="text-gray-500 text-xs">Powered by Llama 3 + FAISS</p>
        <p className="text-gray-600 text-xs mt-1">ANITS Visakhapatnam</p>
      </div>

    </div>
  )
}