import Sidebar from "../Sidebar/Sidebar";

export default function Layout({ children }) {
  return (
    <div className="h-screen w-full flex">
      <Sidebar />
      <div className="flex-1 flex flex-col h-full min-w-0">
        {children}
      </div>
    </div>
  );
}
