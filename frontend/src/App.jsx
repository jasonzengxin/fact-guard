import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import FactCheckForm from './components/FactCheckForm';
import FactCheckResults from './components/FactCheckResults';
import logo from './assets/shield-logo.png';
import './App.css';

const App = () => {
  const [results, setResults] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const handleStartClick = (e) => {
    e.preventDefault();
    setShowForm(true);
    // 平滑滚动到表单位置
    setTimeout(() => {
      document.getElementById('checkForm').scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col">
      <Navbar />
      
      <main className="flex-grow flex flex-col">
        {/* Initial Hero Section - Always visible */}
        <div className={`flex-grow flex items-center justify-center transition-all duration-500 ease-in-out ${
          showForm ? 'h-auto mb-12' : 'min-h-[calc(100vh-8rem)]'
        }`}>
          <div className="text-center px-4">
            <div className="flex justify-center mb-8">
              <div className={`bg-gradient-to-b from-yellow-500/10 to-gray-900 p-4 rounded-xl shadow-2xl transform transition-all duration-500 ${
                showForm ? 'scale-75' : 'hover:scale-105'
              }`}>
                <img src={logo} alt="FactGuard Logo" className={`transition-all duration-500 ${
                  showForm ? 'h-20' : 'h-32'
                } w-auto`} />
              </div>
            </div>
            <h1 className={`font-['Righteous'] tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 to-yellow-600 transition-all duration-500 ${
              showForm ? 'text-3xl mb-2' : 'text-6xl mb-6'
            }`}>
              FactGuard
            </h1>
            <div className={`space-y-2 transition-all duration-500 ${
              showForm ? 'text-base' : 'text-xl'
            }`}>
              <p className="text-gray-400">
                AI驱动的事实核查助手
              </p>
              <p className="text-yellow-500 font-medium">
                帮助您快速验证信息真实性
              </p>
            </div>
            {!showForm && (
              <div className="mt-12 animate-bounce">
                <button 
                  onClick={handleStartClick}
                  className="inline-flex items-center px-8 py-3 text-lg font-medium text-gray-900 bg-gradient-to-r from-yellow-400 to-yellow-500 rounded-lg shadow-lg hover:from-yellow-500 hover:to-yellow-600 transform hover:scale-105 transition-all duration-300"
                >
                  <span>开始使用</span>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Content that appears after clicking start */}
        <div className={`transition-all duration-500 ease-in-out max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 ${
          showForm ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10 pointer-events-none hidden'
        }`}>
          {/* Main Content */}
          <div id="checkForm" className="mb-16">
            <div className="bg-gradient-to-b from-gray-800 to-gray-800/50 shadow-2xl rounded-xl overflow-hidden backdrop-blur-sm">
              <div className="p-6 sm:p-8">
                <FactCheckForm onResultsReceived={setResults} />
                {results && (
                  <div className="mt-8 border-t border-gray-700/50 pt-8">
                    <FactCheckResults results={results} />
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Features Section */}
          <div id="features" className="mb-16">
            <h2 className="text-2xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-yellow-600 mb-12">
              为什么选择 FactGuard
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-br from-gray-800 to-gray-800/50 p-6 rounded-xl shadow-xl hover:shadow-2xl transition-shadow duration-300">
                <div className="text-yellow-500 text-xl mb-4">🎯</div>
                <h3 className="text-lg font-semibold mb-3 text-yellow-400">多源验证</h3>
                <p className="text-sm text-gray-300">
                  采用多个权威来源交叉验证，确保核查结果的准确性和可靠性。
                </p>
              </div>
              <div className="bg-gradient-to-br from-gray-800 to-gray-800/50 p-6 rounded-xl shadow-xl hover:shadow-2xl transition-shadow duration-300">
                <div className="text-yellow-500 text-xl mb-4">⚡️</div>
                <h3 className="text-lg font-semibold mb-3 text-yellow-400">实时分析</h3>
                <p className="text-sm text-gray-300">
                  先进的AI技术支持，秒级响应，快速完成事实核查。
                </p>
              </div>
              <div className="bg-gradient-to-br from-gray-800 to-gray-800/50 p-6 rounded-xl shadow-xl hover:shadow-2xl transition-shadow duration-300">
                <div className="text-yellow-500 text-xl mb-4">🛡️</div>
                <h3 className="text-lg font-semibold mb-3 text-yellow-400">专业可靠</h3>
                <p className="text-sm text-gray-300">
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