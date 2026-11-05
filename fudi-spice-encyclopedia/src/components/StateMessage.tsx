export function Loading() {
  return (
    <p role="status" className="container-page py-16 text-ink/70">
      Loading…
    </p>
  )
}

export function ErrorMessage({ message }: { message: string }) {
  return (
    <p role="alert" className="container-page py-16 font-semibold text-maroon">
      Something went wrong: {message}
    </p>
  )
}
