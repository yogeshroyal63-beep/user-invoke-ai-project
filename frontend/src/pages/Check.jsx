import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ChatContainer from "../components/Chat/ChatContainer";

export default function Check() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/");
  }, []);

  return (
    <div className="h-screen bg-black text-white">
      <ChatContainer />
    </div>
  );
}
