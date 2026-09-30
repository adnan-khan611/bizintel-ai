export default function Loading() {
  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-6 py-8 lg:px-8">
        <header className="mb-8">
          <div className="h-4 w-36 animate-pulse rounded bg-slate-200" />

          <div className="mt-3 h-9 w-56 animate-pulse rounded bg-slate-200" />

          <div className="mt-3 h-5 w-full max-w-2xl animate-pulse rounded bg-slate-200" />
        </header>

        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((card) => (
            <div
              key={card}
              className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
            >
              <div className="h-4 w-20 animate-pulse rounded bg-slate-200" />

              <div className="mt-4 h-9 w-32 animate-pulse rounded bg-slate-200" />

              <div className="mt-3 h-4 w-40 animate-pulse rounded bg-slate-200" />
            </div>
          ))}
        </section>

        <section className="mt-6 grid gap-6 lg:grid-cols-2">
          {[1, 2].map((card) => (
            <div
              key={card}
              className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
            >
              <div className="h-6 w-40 animate-pulse rounded bg-slate-200" />

              <div className="mt-3 h-4 w-64 animate-pulse rounded bg-slate-200" />

              <div className="mt-6 h-64 animate-pulse rounded-lg bg-slate-100" />
            </div>
          ))}
        </section>
      </div>
    </main>
  );
}