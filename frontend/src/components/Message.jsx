import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
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

  const markdownComponents = {
    code({ inline, className, children, ...props }) {
      const match = /language-(\w+)/.exec(className || "");

      if (!inline && match) {
        return (
          <SyntaxHighlighter
            style={oneDark}
            language={match[1]}
            PreTag="div"
            customStyle={{ margin: 0, borderRadius: "0.75rem" }}
            {...props}
          >
            {String(children).replace(/\n$/, "")}
          </SyntaxHighlighter>
        );
      }

      return (
        <code className={className} {...props}>
          {children}
        </code>
      );
    },
  };

  return (
    <div className="px-4 py-4 sm:px-0">
      <div className={`group rounded-[1.75rem] border border-white/10 px-4 py-4 shadow-sm transition ${isUser ? "bg-white/[0.02]" : "bg-white/[0.04]"}`}>
        <div className="flex gap-4">
          <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl text-sm font-semibold ${isUser ? "bg-sky-500 text-white" : "bg-white/10 text-white"}`}>
            {isUser ? "U" : "S"}
          </div>
          <div className="min-w-0 flex-1 space-y-3">
            <div className="text-xs font-medium uppercase tracking-[0.28em] text-gray-500">
              {isUser ? "You" : "Summer"}
            </div>

            {toolCalls && toolCalls.length > 0 && (
              <div className="flex flex-wrap gap-2 py-0.5">
                {toolCalls.map((tc, idx) => (
                  <ToolBadge key={idx} name={tc.function?.name || tc.name} />
                ))}
              </div>
            )}

            {thinking && (
              <details open={!reply} className="overflow-hidden rounded-2xl border border-white/10 bg-black/20">
                <summary className="flex cursor-pointer items-center justify-between px-4 py-2.5 text-xs font-medium text-gray-400 select-none hover:bg-white/[0.03]">
                  <span className="flex items-center gap-2">
                    <span className={`h-1.5 w-1.5 rounded-full bg-sky-400 ${!reply ? "animate-pulse" : ""}`}></span>
                    Thinking
                  </span>
                  <span className="text-[10px] transition-transform duration-200 group-open:rotate-180">
                    ▼
                  </span>
                </summary>
                <div className="border-t border-white/10 px-4 pb-3 pt-2 text-xs leading-relaxed text-gray-500 whitespace-pre-wrap">
                  {thinking}
                </div>
              </details>
            )}

            <div className="prose prose-invert max-w-none prose-sm text-gray-100 prose-p:my-2 prose-pre:p-0 prose-pre:bg-transparent prose-code:text-inherit">
              {reply ? (
                <ReactMarkdown components={markdownComponents}>{reply}</ReactMarkdown>
              ) : (
                !thinking && <span className="text-gray-500 italic">Thinking...</span>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
