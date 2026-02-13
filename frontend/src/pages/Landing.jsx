import Navbar from "../components/Navbar";
import HeroSection from "../components/HeroSection";
import Features from "../components/Features";
import PrivacySection from "../components/PrivacySection";
import CTASection from "../components/CTASection";
import Footer from "../components/Footer";

export default function Landing() {
  return (
    
    <div className="min-h-screen bg-gradient-to-br from-[#020617] via-[#050b18] to-[#020617] text-slate-100">
      <Navbar />
      <HeroSection />
      <Features />
      <PrivacySection />
      <CTASection />
      <Footer />
      
    </div>
  );
}
