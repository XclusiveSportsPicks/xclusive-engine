// frontend/pages/_error.js
export default function Error({ statusCode }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-6 rounded shadow">
        <h1 className="text-2xl font-bold mb-4">
          {statusCode
            ? `An error ${statusCode} occurred on server`
            : 'An error occurred on client'}
        </h1>
        <p>Please try refreshing the page.</p>
      </div>
    </div>
  )
}

Error.getInitialProps = ({ res, err }) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404
  return { statusCode }
}
