import Provider from "@/redux/Provider";
import Navbar from "@/components/Navbar";
import Setup from "@/utils/Setup";
import "../globals.css";
import Setup from "@/utils/Setup";

export const metadata = {
  title: "Next.js",
  description: "Generated by Next.js",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Provider>
          <div className="max-w-6xl mx-auto">
            <Navbar />
            <div>{children}</div>
            <Setup />
          </div>
        </Provider>
      </body>
    </html>
  );
}
