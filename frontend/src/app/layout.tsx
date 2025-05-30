import "./globals.css";
import NavigationBar from "@/components/NavigationBar";
import Footer from "@/components/Footer";

export const metadata = {
  title: "NewMind",
  description: "NewMind Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-[#18181b] min-h-screen flex flex-col">
        <NavigationBar />
        <main className="flex-1 flex flex-col">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
