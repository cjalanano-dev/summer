import ToolBadge from "./ToolBadge";

function parseMessageContent(content) {
  if (!content) return { thinking: "", reply: "" };

  let temp = content;
  let thinkingParts = [];
  let reply = "";

  while (true) {
    const thinkStartRegex = /<think>/i;
    const startMatch = temp.match(thinkStartRegex);
    if (!startMatch) {
      reply += temp;
      break;
    }

    const startIdx = startMatch.index;
    reply += temp.slice(0, startIdx);

    const afterStart = temp.slice(startIdx + startMatch[0].length);
    const thinkEndRegex = /<\/think>/i;
    const endMatch = afterStart.match(thinkEndRegex);

    if (!endMatch) {
      // Still thinking/unclosed tag
      thinkingParts.push(afterStart);
      break;
    }

    const endIdx = endMatch.index;
    thinkingParts.push(afterStart.slice(0, endIdx));
    temp = afterStart.slice(endIdx + endMatch[0].length);
  }

  return {
    thinking: thinkingParts.join("\n").trim(),
    reply: reply.trim()
  };
}

export default function Message({ role, content, toolCalls }) {
  const isUser = role === "user";
  const { thinking, reply } = parseMessageContent(content);

  return (
    <div className={`py-6 px-4 md:px-8 border-b border-gray-900 ${isUser ? "bg-gray-950" : "bg-gray-900/60"}`}>
      <div className="max-w-3xl mx-auto flex gap-4">
        <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${isUser ? "bg-blue-600 text-white" : "bg-purple-600 text-white"}`}>
          {isUser ? "U" : "S"}
        </div>
        
        <div className="flex-1 space-y-3">
          <div className="text-sm font-semibold text-gray-400 capitalize">
            {isUser ? "You" : "Summer"}
          </div>
          
          {toolCalls && toolCalls.length > 0 && (
            <div className="flex flex-wrap gap-2 py-1">
              {toolCalls.map((tc, idx) => (
                <ToolBadge key={idx} name={tc.function?.name || tc.name} />
              ))}
            </div>
          )}

          {thinking && (
            <details open={!reply} className="group border border-gray-800 bg-gray-950/40 rounded-lg overflow-hidden">
              <summary className="flex items-center justify-between px-4 py-2.5 text-xs font-medium text-gray-400 cursor-pointer hover:bg-gray-800/30 select-none">
                <span className="flex items-center gap-2">
                  <span className={`w-1.5 h-1.5 rounded-full bg-purple-500 ${!reply ? "animate-pulse" : ""}`}></span>
                  Thinking Process
                </span>
                <span className="transition-transform duration-200 group-open:rotate-180 text-[10px]">
                  ▼
                </span>
              </summary>
              <div className="px-4 pb-3 pt-1 text-xs text-gray-500 border-t border-gray-900 whitespace-pre-wrap font-mono leading-relaxed">
                {thinking}
              </div>
            </details>
          )}

          <div className="text-gray-100 leading-relaxed whitespace-pre-wrap text-sm md:text-base">
            {reply || (!thinking && <span className="text-gray-500 italic">Thinking...</span>)}
          </div>
        </div>
      </div>
    </div>
  );
}
