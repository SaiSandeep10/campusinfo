export default function Sidebar({ isOpen, onToggle }) {
  const categories = [
    { icon: '🏫', label: 'About ANITS' },
    { icon: '📚', label: 'Departments' },
    { icon: '🎓', label: 'Admissions' },
    { icon: '💼', label: 'Placements' },
    { icon: '🏢', label: 'Facilities' },
    { icon: '🎭', label: 'Clubs & Events' },
    { icon: '📞', label: 'Contacts' },
    { icon: '🗺️', label: 'Campus Map' },
  ];

  if (!isOpen) return null;

  return (
    <aside className="w-64 bg-gray-900 border-r border-gray-700 flex flex-col h-screen">
      <div className="px-4 py-5 border-b border-gray-700">
        <h2 className="text-white font-bold text-lg">🎓 ANITS</h2>
        <p className="text-gray-400 text-xs mt-1">Campus Information Assistant</p>
      </div>
      <div className="flex-1 overflow-y-auto px-3 py-4">
        <p className="text-gray-500 text-xs uppercase tracking-wider mb-3 px-2">
          Categories
        </p>
        {categories.map((cat, i) => (
          <button
            key={i}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-gray-300 hover:bg-gray-800 hover:text-white transition text-sm text-left mb-1"
          >
            <span>{cat.icon}</span>
            <span>{cat.label}</span>
          </button>
        ))}
      </div>
      <div className="px-4 py-4 border-t border-gray-700">
        <p className="text-gray-600 text-xs text-center">Powered by Groq Llama 3</p>
        <p className="text-gray-600 text-xs text-center mt-1">ANITS Visakhapatnam</p>
      </div>
    </aside>
  );
}