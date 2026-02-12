import Navbar from "../components/Navbar";
import ExampleCards from "../components/ExampleCards";
import ChatContainer from "../components/Chat/ChatContainer";

export default function Check() {
  return (
    <div className="min-h-screen bg-[#020617] text-slate-100">
      <Navbar />
      <div className="text-center py-10">
        <h1 className="text-3xl font-bold">Security Check Assistant</h1>
        <p className="text-slate-400 mt-2">
          Paste any message, link, or situation to analyze risk
        </p>
      </div>
      <ExampleCards />
      <ChatContainer />
    </div>
  );
}
