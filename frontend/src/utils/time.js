export function formatRelativeTime(isoString) {
  const now = Date.now();
  const then = new Date(isoString).getTime();
  const diffMs = now - then;
  const diffSec = Math.floor(diffMs / 1000);

  if (diffSec < 60) return "Just now";
  if (diffSec < 3600) return `${Math.floor(diffSec / 60)} min ago`;
  if (diffSec < 86400) return `${Math.floor(diffSec / 3600)} hr ago`;
  if (diffSec < 604800) {
    const days = Math.floor(diffSec / 86400);
    return days === 1 ? "Yesterday" : `${days} days ago`;
  }

  const d = new Date(then);
  const nowYear = new Date(now).getFullYear();
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const monthDay = `${months[d.getMonth()]} ${d.getDate()}`;
  if (d.getFullYear() === nowYear) return monthDay;
  return `${monthDay}, ${d.getFullYear()}`;
}
