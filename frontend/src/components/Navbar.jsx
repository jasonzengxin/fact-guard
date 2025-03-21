import React from 'react';
import logo from '../assets/shield-logo.png';

const Navbar = () => {
  return (
    <nav className="bg-gray-900 border-b border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="flex items-center gap-2 bg-gradient-to-r from-gray-800 to-gray-900 p-2 rounded-lg">
                <img src={logo} alt="FactGuard Logo" className="h-8 w-auto" />
                <span className="text-2xl font-bold text-yellow-500">FactGuard</span>
              </div>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <a href="#" className="text-gray-300 hover:text-yellow-500 px-3 py-2 rounded-md text-sm font-medium">
                  首页
                </a>
                <a href="#about" className="text-gray-300 hover:text-yellow-500 px-3 py-2 rounded-md text-sm font-medium">
                  关于
                </a>
                <a href="#api" className="text-gray-300 hover:text-yellow-500 px-3 py-2 rounded-md text-sm font-medium">
                  API
                </a>
              </div>
            </div>
          </div>
          <div className="hidden md:block">
            <div className="ml-4 flex items-center md:ml-6">
              <button className="bg-yellow-500 text-gray-900 px-4 py-2 rounded-md text-sm font-medium hover:bg-yellow-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500">
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