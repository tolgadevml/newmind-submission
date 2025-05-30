"use client";
import Link from "next/link";

export default function NavigationBar() {
  return (
    <nav className="w-full bg-black text-white py-4 px-8 flex items-center">
      <Link href="/" className="text-2xl font-bold tracking-wide hover:text-gray-300 transition-colors">
        NewMind
      </Link>
    </nav>
  );
}
