export default function Message({ message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} max-w-3xl mx-auto w-full`}>
      <div className={`flex gap-3 max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm flex-shrink-0 ${isUser ? 'bg-blue-600' : 'bg-green-700'}`}>
          {isUser ? '👤' : '🎓'}
        </div>
        <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${isUser ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-gray-800 text-gray-100 rounded-tl-none'}`}>
          <p className="whitespace-pre-wrap">{message.content}</p>
          <p className={`text-xs mt-1 ${isUser ? 'text-blue-200' : 'text-gray-500'}`}>
            {message.timestamp}
          </p>
        </div>
      </div>
    </div>
  );
}