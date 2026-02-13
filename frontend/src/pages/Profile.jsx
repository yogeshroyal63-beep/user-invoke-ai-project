import { useNavigate } from "react-router-dom";

export default function Profile() {

  const navigate = useNavigate();
  const email = "user@example.com"; // demo placeholder

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center">

      <div className="bg-gray-900 p-10 rounded-2xl w-[420px] shadow-2xl">

        <h2 className="text-2xl font-bold mb-6 text-center">
          User Profile
        </h2>

        <div className="space-y-4">

          <div className="bg-gray-800 p-4 rounded-lg">
            <p className="text-gray-400 text-sm">Email</p>
            <p className="text-lg">{email}</p>
          </div>

          <div className="bg-gray-800 p-4 rounded-lg">
            <p className="text-gray-400 text-sm">Account Type</p>
            <p className="text-lg">Free Tier</p>
          </div>

        </div>

        <button
          onClick={() => navigate("/check")}
          className="mt-6 w-full bg-blue-600 hover:bg-blue-700 p-3 rounded-lg"
        >
          Back to Dashboard
        </button>

      </div>
    </div>
  );
}
