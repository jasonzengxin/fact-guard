import React, { useState } from 'react';
import FactCheckForm from './components/FactCheckForm';
import FactCheckResults from './components/FactCheckResults';

const App = () => {
  const [results, setResults] = useState(null);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <header className="bg-gray-800 shadow-lg">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-yellow-500">
            FactGuard
          </h1>
          <p className="mt-2 text-gray-400">
            AI驱动的事实核查助手
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <FactCheckForm onResultsReceived={setResults} />
          {results && <FactCheckResults results={results} />}
        </div>
      </main>

      <footer className="bg-gray-800 mt-auto">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-400 text-sm">
            © 2024 FactGuard. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App; 