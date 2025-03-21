import React from 'react';

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

const FactCheckResults = ({ results }) => {
  if (!results) return null;

  const {
    is_fact,
    confidence: confidenceScore,
    explanation,
    sources = [],
    academic_sources = [],
    discrepancies = []
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
    </div>
  );
};

export default FactCheckResults; 