import { useEffect } from "react";
import { useChatStore } from "./store/chatStore";
import Layout from "./components/Layout/Layout";
import TopBar from "./components/Layout/TopBar";
import ChatWindow from "./components/Chat/ChatWindow";
import InputBox from "./components/Chat/InputBox";
import ConfirmModal from "./components/Common/ConfirmModal";

export default function App() {
  const bootstrap = useChatStore((s) => s.bootstrap);

  useEffect(() => {
    bootstrap();
  }, []);

  return (
    <div className="h-screen w-full overflow-hidden bg-black text-neutral-300">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.03),_transparent_30%),radial-gradient(circle_at_top_right,_rgba(255,255,255,0.02),_transparent_24%),linear-gradient(180deg,_rgba(20,20,20,1),_rgba(0,0,0,1))]" />
      <div className="relative h-full w-full flex">
        <Layout>
          <TopBar />
          <ChatWindow />
          <InputBox />
        </Layout>
      </div>
      <ConfirmModal />
    </div>
  );
}
