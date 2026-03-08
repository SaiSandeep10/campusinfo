export default function Message({ message, onSuggestionClick }) {

  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>

      <div
        className={`max-w-xl px-4 py-3 rounded-xl ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-gray-800 text-gray-200"
        }`}
      >

        {/* Message text */}
        <p className="text-sm whitespace-pre-wrap">
          {message.content}
        </p>

        {/* Images */}
        {message.media?.images && (
          <div className="flex gap-2 flex-wrap mt-3">
            {message.media.images.map((img, i) => (
              <img
                key={i}
                src={img}
                alt="media"
                className="w-32 rounded-lg border border-gray-600"
              />
            ))}
          </div>
        )}

        {/* Video */}
        {message.media?.video && (
          <a
            href={message.media.video}
            target="_blank"
            rel="noopener noreferrer"
            className="block text-blue-400 underline mt-2 text-sm"
          >
            ▶ Watch related video
          </a>
        )}

        {/* Recommendations */}
        {message.recommendations && message.recommendations.length > 0 && (
          <div className="mt-3">
            <p className="text-xs text-gray-400 mb-1">
              You may also ask:
            </p>

            <div className="flex flex-wrap gap-2">
              {message.recommendations.map((q, i) => (
                <button
                  key={i}
                  onClick={() => onSuggestionClick(q)}
                  className="px-2 py-1 bg-gray-700 hover:bg-gray-600 text-xs rounded text-gray-200"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Timestamp */}
        <div className="text-xs text-gray-500 mt-2">
          {message.timestamp}
        </div>

      </div>

    </div>
  );
}