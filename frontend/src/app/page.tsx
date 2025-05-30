'use client';
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  return (
    <div className="flex flex-1 flex-col justify-center items-center min-h-[60vh] bg-[#18181b]">
      <h1 className="text-4xl font-bold text-white mb-6">Welcome!</h1>
      <button
        className="px-8 py-4 rounded-xl text-white text-xl font-semibold bg-gradient-to-r from-blue-500 via-cyan-400 to-blue-600 animate-gradient-move shadow-lg transition-transform hover:scale-105"
        onClick={() => router.push('/analyze')}
      >
        Start Analysis
      </button>
    </div>
  );
}
