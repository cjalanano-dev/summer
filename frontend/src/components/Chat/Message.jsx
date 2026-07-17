import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import ToolBadge from "../Common/ToolBadge";

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
    reply += temp.slice(0, startMatch.index);
    const afterStart = temp.slice(startMatch.index + startMatch[0].length);
    const thinkEndRegex = /<\/think>/i;
    const endMatch = afterStart.match(thinkEndRegex);

    if (!endMatch) {
      thinkingParts.push(afterStart);
      break;
    }

    thinkingParts.push(afterStart.slice(0, endMatch.index));
    temp = afterStart.slice(endMatch.index + endMatch[0].length);
  }

  return {
    thinking: thinkingParts.join("\n").trim(),
    reply: reply.trim(),
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
      return <code className={className} {...props}>{children}</code>;
    },
  };

  return (
    <div className="group px-4 py-3 sm:px-0">
      <div className="flex items-start gap-4">
        <div
          className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-sm font-semibold ${
            isUser ? "bg-neutral-700 text-white" : "bg-neutral-800 text-neutral-300"
          }`}
        >
          {isUser ? "U" : "S"}
        </div>
        <div className="min-w-0 flex-1 space-y-2 pt-1">
          <div className="text-xs font-medium uppercase tracking-[0.15em] text-neutral-600">
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
            <details
              open={!reply}
              className="overflow-hidden rounded-xl border border-neutral-800 bg-neutral-950"
            >
              <summary className="flex cursor-pointer items-center justify-between px-4 py-2.5 text-xs font-medium text-neutral-500 select-none hover:bg-neutral-900">
                <span className="flex items-center gap-2">
                  <span
                    className={`h-1.5 w-1.5 rounded-full bg-neutral-500 ${
                      !reply ? "animate-pulse" : ""
                    }`}
                  ></span>
                  Thinking
                </span>
                <span className="text-[10px] transition-transform duration-200 group-open:rotate-180">
                  ▼
                </span>
              </summary>
              <div className="border-t border-neutral-800 px-4 pb-3 pt-2 text-xs leading-relaxed text-neutral-500 whitespace-pre-wrap">
                {thinking}
              </div>
            </details>
          )}

          <div className="prose prose-invert max-w-none prose-sm text-neutral-200 prose-p:my-2 prose-pre:p-0 prose-pre:bg-transparent prose-code:text-inherit">
            {reply ? (
              <ReactMarkdown components={markdownComponents}>{reply}</ReactMarkdown>
            ) : (
              !thinking && (
                <span className="text-neutral-600 italic">Thinking...</span>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
