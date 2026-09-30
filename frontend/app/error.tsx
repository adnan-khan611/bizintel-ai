"use client";

import { useEffect } from "react";

interface ErrorPageProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ErrorPage({
  error,
  reset,
}: ErrorPageProps) {
  useEffect(() => {
    console.error("Dashboard error:", error);
  }, [error]);

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto flex min-h-screen max-w-2xl items-center px-6 py-8">
        <section className="w-full rounded-xl border border-red-200 bg-white p-8 text-center shadow-sm">
          <div className="text-4xl" aria-hidden="true">
            ⚠️
          </div>

          <h1 className="mt-4 text-xl font-semibold text-slate-900">
            Dashboard unavailable
          </h1>

          <p className="mt-3 text-sm leading-6 text-slate-600">
            We could not load the business analytics right now.
            Please make sure the backend API is running and try again.
          </p>

          <button
            type="button"
            onClick={() => reset()}
            className="mt-6 rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700"
          >
            Try again
          </button>
        </section>
      </div>
    </main>
  );
}