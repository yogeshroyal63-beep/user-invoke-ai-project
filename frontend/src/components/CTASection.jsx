import { Link } from "react-router-dom";

export default function CTASection() {
  return (
    <section className="bg-gradient-to-r from-blue-600 to-indigo-600 text-center py-16">
      <h2 className="text-3xl font-bold mb-4">Ready to Stay Safe?</h2>
      <Link
        to="/check"
        className="bg-white text-black px-8 py-3 rounded-xl font-semibold"
      >
        Start Checking Now
      </Link>
    </section>
  );
}
