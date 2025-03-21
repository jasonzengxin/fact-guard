import React from 'react';
import Logo from './Logo';

const Footer = () => {
  return (
    <footer className="bg-gray-800 border-t border-gray-700">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2">
              <Logo className="h-8 w-8 text-yellow-500" />
              <span className="text-2xl font-bold text-yellow-500">FactGuard</span>
            </div>
            <p className="mt-4 text-gray-400 max-w-md">
              FactGuard 是一个基于人工智能的事实核查助手，帮助您快速验证信息的真实性，
              打击虚假信息传播，维护信息生态的健康发展。
            </p>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">产品</h3>
            <ul className="mt-4 space-y-4">
              <li>
                <a href="#features" className="text-gray-300 hover:text-yellow-500">
                  功能特点
                </a>
              </li>
              <li>
                <a href="#pricing" className="text-gray-300 hover:text-yellow-500">
                  价格方案
                </a>
              </li>
              <li>
                <a href="#api" className="text-gray-300 hover:text-yellow-500">
                  API 文档
                </a>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">支持</h3>
            <ul className="mt-4 space-y-4">
              <li>
                <a href="#help" className="text-gray-300 hover:text-yellow-500">
                  帮助中心
                </a>
              </li>
              <li>
                <a href="#contact" className="text-gray-300 hover:text-yellow-500">
                  联系我们
                </a>
              </li>
              <li>
                <a href="#privacy" className="text-gray-300 hover:text-yellow-500">
                  隐私政策
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-gray-700">
          <p className="text-center text-gray-400 text-sm">
            © {new Date().getFullYear()} FactGuard. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 