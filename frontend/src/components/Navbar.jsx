import React from 'react';

const Navbar = () => {
  return (
    <nav className="bg-gray-900 border-b border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="hidden md:block">
              <div className="flex items-baseline space-x-4">
                <a href="#" className="text-gray-300/50 hover:text-yellow-500 px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 blur-[1px] hover:blur-none">
                  首页
                </a>
                <a href="#about" className="text-gray-300/50 hover:text-yellow-500 px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 blur-[1px] hover:blur-none">
                  关于
                </a>
                <a href="#api" className="text-gray-300/50 hover:text-yellow-500 px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 blur-[1px] hover:blur-none">
                  API
                </a>
              </div>
            </div>
          </div>
          <div className="hidden md:block">
            <div className="flex items-center">
              <button className="bg-yellow-500 text-gray-900 px-4 py-2 rounded-md text-sm font-medium hover:bg-yellow-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-all duration-300 hover:scale-105">
                开始使用
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 