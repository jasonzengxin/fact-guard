import React, { useState } from 'react';
import ClaimTag from './ClaimTag';

const ITEMS_PER_PAGE = 3;

const getConfidenceColor = (confidence) => {
  if (!confidence) return 'text-gray-600';
  if (confidence > 0.7) return 'text-green-600';
  if (confidence > 0.4) return 'text-yellow-600';
  return 'text-red-600';
};

const SourceCard = ({ source }) => {
  const contributionScore = (source.contribution_score || 0) * 100;
  const scoreColor = contributionScore > 70 ? 'text-green-600' : 
                    contributionScore > 40 ? 'text-yellow-600' : 'text-red-600';
  
  const typeColor = source.source_type === 'academic' ? 'bg-blue-100 text-blue-800' :
                   source.source_type === 'government' ? 'bg-green-100 text-green-800' :
                   'bg-gray-100 text-gray-800';
  
  const sourceType = source.source_type === 'academic' ? '学术来源' : 
                    source.source_type === 'government' ? '政府来源' : '其他来源';

  return (
    <div className="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition duration-200 mb-4">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center mb-2">
            <h4 className="font-medium text-gray-800 mr-2">{source.title || '未命名来源'}</h4>
            <span className={`text-sm ${typeColor} px-2 py-1 rounded-full`}>{sourceType}</span>
          </div>
          <p className="text-sm text-gray-600 mb-2">{source.snippet || '无内容摘要'}</p>
          {source.link && (
            <a
              href={source.link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 text-sm inline-flex items-center"
            >
              <i className="fas fa-external-link-alt mr-1" />
              查看原文
            </a>
          )}
        </div>
        <div className="ml-4">
          <div className={`text-sm ${scoreColor} font-medium bg-white px-3 py-1 rounded-full shadow-sm`}>
            贡献度: {contributionScore.toFixed(1)}%
          </div>
        </div>
      </div>
    </div>
  );
};

const DiscrepancyCard = ({ discrepancy }) => {
  return (
    <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-red-500 mb-4">
      <div className="mb-4">
        <h4 className="text-lg font-medium text-gray-800 mb-2">声明</h4>
        <p className="text-gray-600">{discrepancy.claim}</p>
      </div>
      
      <div className="mb-4">
        <h4 className="text-lg font-medium text-gray-800 mb-2">矛盾来源</h4>
        <SourceCard source={discrepancy.source} />
      </div>
      
      <div>
        <h4 className="text-lg font-medium text-gray-800 mb-2">解释</h4>
        <p className="text-gray-600">{discrepancy.explanation}</p>
      </div>
    </div>
  );
};

const ClaimsList = ({ claims }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [expandedClaims, setExpandedClaims] = useState({});
  
  const totalPages = Math.ceil(claims.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const currentClaims = claims.slice(startIndex, endIndex);

  const toggleClaim = (index) => {
    setExpandedClaims(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  return (
    <div>
      <div className="space-y-2">
        {currentClaims.map((claim, index) => (
          <div key={index} className="bg-gray-800 p-4 rounded-lg flex items-start justify-between group">
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-3">
                <span className="flex-shrink-0 w-6 h-6 bg-gray-700 rounded-full flex items-center justify-center text-gray-300 text-sm">
                  {startIndex + index + 1}
                </span>
                <p className="text-gray-200 text-sm break-words">{claim.claim}</p>
              </div>
              <div className="mt-2 flex items-center space-x-2">
                <ClaimTag tag={claim.tag} />
              </div>
            </div>
            <button
              onClick={() => toggleClaim(index)}
              className="ml-3 text-gray-400 hover:text-white focus:outline-none flex-shrink-0"
            >
              <svg
                className={`w-5 h-5 transform transition-transform ${expandedClaims[index] ? 'rotate-180' : ''}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>
        ))}
      </div>

      {/* 始终显示分页控件 */}
      <div className="mt-4 flex items-center justify-between px-2">
        <div className="flex-1 flex justify-between sm:hidden">
          <button
            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
            className="px-3 py-1 rounded-md bg-gray-700 text-sm text-white disabled:opacity-50"
          >
            上一页
          </button>
          <span className="text-sm text-gray-400">
            {currentPage} / {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
            className="px-3 py-1 rounded-md bg-gray-700 text-sm text-white disabled:opacity-50"
          >
            下一页
          </button>
        </div>
        <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p className="text-sm text-gray-400">
              第 <span className="font-medium text-gray-200">{startIndex + 1}</span> - 
              <span className="font-medium text-gray-200">{Math.min(endIndex, claims.length)}</span> 条，
              共 <span className="font-medium text-gray-200">{claims.length}</span> 条
            </p>
          </div>
          <div>
            <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <button
                onClick={() => setCurrentPage(1)}
                disabled={currentPage === 1}
                className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-600 bg-gray-700 text-sm font-medium text-gray-300 hover:bg-gray-600 disabled:opacity-50"
              >
                <span className="sr-only">首页</span>
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M15.707 15.707a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 010 1.414zm-6 0a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 011.414 1.414L5.414 10l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
                </svg>
              </button>
              <button
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                className="relative inline-flex items-center px-2 py-2 border border-gray-600 bg-gray-700 text-sm font-medium text-gray-300 hover:bg-gray-600 disabled:opacity-50"
              >
                <span className="sr-only">上一页</span>
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </button>
              <span className="relative inline-flex items-center px-4 py-2 border border-gray-600 bg-gray-700 text-sm font-medium text-gray-300">
                {currentPage} / {totalPages}
              </span>
              <button
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
                className="relative inline-flex items-center px-2 py-2 border border-gray-600 bg-gray-700 text-sm font-medium text-gray-300 hover:bg-gray-600 disabled:opacity-50"
              >
                <span className="sr-only">下一页</span>
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </button>
              <button
                onClick={() => setCurrentPage(totalPages)}
                disabled={currentPage === totalPages}
                className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-600 bg-gray-700 text-sm font-medium text-gray-300 hover:bg-gray-600 disabled:opacity-50"
              >
                <span className="sr-only">末页</span>
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 15.707a1 1 0 001.414 0l5-5a1 1 0 000-1.414l-5-5a1 1 0 00-1.414 1.414L8.586 10l-4.293 4.293a1 1 0 000 1.414zm6 0a1 1 0 001.414 0l5-5a1 1 0 000-1.414l-5-5a1 1 0 00-1.414 1.414L14.586 10l-4.293 4.293a1 1 0 000 1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
};

const FactCheckResults = ({ results }) => {
  if (!results) return null;

  const {
    is_fact,
    confidence: confidenceScore,
    explanation,
    sources = [],
    academic_sources = [],
    discrepancies = [],
    claims = []
  } = results;

  const allSources = [...sources, ...academic_sources].sort(
    (a, b) => (b.contribution_score || 0) - (a.contribution_score || 0)
  );

  return (
    <div className="space-y-8 animate__animated animate__fadeIn">
      {/* 核查结果状态 */}
      <div className="bg-white rounded-lg p-6 shadow-lg">
        <div className="flex items-center mb-4">
          <span className="text-3xl mr-3">
            {is_fact ? '✅' : '❌'}
          </span>
          <h2 className={`text-xl font-semibold ${is_fact ? 'text-green-600' : 'text-red-600'}`}>
            {is_fact ? '基本准确' : '可能不准确'}
          </h2>
        </div>
        
        <div className={`mt-2 ${getConfidenceColor(confidenceScore)}`}>
          可信度: {Math.round((confidenceScore || 0) * 100)}%
        </div>
        
        <p className="mt-4 text-gray-600">{explanation}</p>
      </div>

      {/* 来源列表 */}
      <div className="bg-white rounded-lg p-6 shadow-lg">
        <h3 className="text-xl font-semibold mb-4">信息来源</h3>
        <div className="space-y-4">
          {allSources.length > 0 ? (
            allSources.map((source, index) => (
              <SourceCard key={index} source={source} />
            ))
          ) : (
            <div className="bg-gray-50 rounded-lg p-4 text-center">
              <i className="fas fa-info-circle text-gray-400 text-2xl mb-2" />
              <p className="text-gray-500">未找到相关来源</p>
            </div>
          )}
        </div>
      </div>

      {/* 矛盾点 */}
      {discrepancies.length > 0 && (
        <div className="bg-white rounded-lg p-6 shadow-lg">
          <h3 className="text-xl font-semibold mb-4">发现的矛盾</h3>
          <div className="space-y-4">
            {discrepancies.map((discrepancy, index) => (
              <DiscrepancyCard key={index} discrepancy={discrepancy} />
            ))}
          </div>
        </div>
      )}

      {/* 声明列表 */}
      <div className="bg-white rounded-lg p-6 shadow-lg">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-semibold">待核实声明</h3>
          <span className="text-sm text-gray-500">共 {claims.length} 条</span>
        </div>
        <ClaimsList claims={claims} />
      </div>
    </div>
  );
};

export default FactCheckResults; 