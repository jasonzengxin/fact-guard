import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import FactCheckForm from './components/FactCheckForm';
import FactCheckResults from './components/FactCheckResults';
import logo from './assets/shield-logo.png';
import './App.css';

const App = () => {
  const [results, setResults] = useState(null);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col">
      <Navbar />
      
      <main className="flex-grow">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <div className="flex justify-center mb-6">
              <div className="bg-gradient-to-r from-gray-800 to-gray-900 p-4 rounded-lg shadow-xl">
                <img src={logo} alt="FactGuard Logo" className="h-32 w-auto" />
              </div>
            </div>
            <h1 className="text-4xl font-extrabold text-yellow-500 sm:text-5xl md:text-6xl">
              FactGuard
            </h1>
            <p className="mt-3 max-w-md mx-auto text-xl text-gray-300 sm:text-2xl md:mt-5 md:max-w-3xl">
              AI驱动的事实核查助手，帮助您快速验证信息真实性
            </p>
            <div className="mt-10 flex justify-center space-x-6">
              <a href="#features" className="bg-yellow-500 text-gray-900 px-8 py-3 rounded-md text-base font-medium hover:bg-yellow-400">
                了解更多
              </a>
              <a href="#api" className="border border-yellow-500 text-yellow-500 px-8 py-3 rounded-md text-base font-medium hover:bg-yellow-500 hover:text-gray-900">
                API 文档
              </a>
            </div>
          </div>

          {/* Main Content */}
          <div className="mt-16">
            <div className="bg-gray-800 shadow-xl rounded-lg overflow-hidden">
              <div className="p-6 sm:p-8">
                <FactCheckForm onResultsReceived={setResults} />
                {results && (
                  <div className="mt-8 border-t border-gray-700 pt-8">
                    <FactCheckResults results={results} />
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Features Section */}
          <div id="features" className="mt-24">
            <h2 className="text-3xl font-bold text-center text-yellow-500 mb-12">
              为什么选择 FactGuard
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-gray-800 p-6 rounded-lg">
                <div className="text-yellow-500 text-xl mb-4">🎯 精准核查</div>
                <h3 className="text-xl font-semibold mb-2">多源验证</h3>
                <p className="text-gray-400">
                  采用多个权威来源交叉验证，确保核查结果的准确性和可靠性。
                </p>
              </div>
              <div className="bg-gray-800 p-6 rounded-lg">
                <div className="text-yellow-500 text-xl mb-4">⚡️ 快速响应</div>
                <h3 className="text-xl font-semibold mb-2">实时分析</h3>
                <p className="text-gray-400">
                  先进的AI技术支持，秒级响应，快速完成事实核查。
                </p>
              </div>
              <div className="bg-gray-800 p-6 rounded-lg">
                <div className="text-yellow-500 text-xl mb-4">🛡️ 可信赖</div>
                <h3 className="text-xl font-semibold mb-2">专业可靠</h3>
                <p className="text-gray-400">
                  基于学术研究和权威数据，提供专业的事实核查服务。
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default App; 