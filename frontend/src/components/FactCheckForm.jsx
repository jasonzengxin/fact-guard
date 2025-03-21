import React, { useState } from 'react';
import ClaimItem from './ClaimItem';

const API_URL = 'http://localhost:8000';

const FactCheckForm = ({ onResultsReceived }) => {
  const [text, setText] = useState('');
  const [url, setUrl] = useState('');
  const [claims, setClaims] = useState([]);
  const [originalText, setOriginalText] = useState('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [showPreview, setShowPreview] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!text && !url) {
      alert('请输入要核查的文本或链接');
      return;
    }

    try {
      setLoading(true);
      setShowPreview(false);
      setProgress(0);
      setCurrentStep(0);

      // 模拟进度更新
      const progressInterval = setInterval(() => {
        setProgress(prev => prev < 90 ? prev + 5 : prev);
      }, 500);

      // 提取声明
      const extractResponse = await fetch(`${API_URL}/extract_claims`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          text: text || null,
          url: url || null
        })
      });

      if (!extractResponse.ok) {
        throw new Error('提取声明失败');
      }

      const extractData = await extractResponse.json();
      clearInterval(progressInterval);
      setProgress(100);
      
      setOriginalText(text || url);
      
      const extractedClaims = extractData.claims || [];
      if (extractedClaims.length === 0) {
        alert('未找到有效的待核实内容，请重新输入');
        return;
      }

      setClaims(extractedClaims);
      setShowPreview(true);
    } catch (error) {
      console.error('Error:', error);
      alert('提取声明时出错，请重试');
    } finally {
      setLoading(false);
      setProgress(0);
    }
  };

  const handleConfirm = async () => {
    if (claims.length === 0) {
      alert('请至少选择一个待核实的点');
      return;
    }

    try {
      setLoading(true);
      setShowPreview(false);
      setCurrentStep(1);
      setProgress(0);

      // 准备请求数据
      const requestData = {
        text: text || null,
        url: url || null,
        claims
      };

      // 搜索相关来源
      let searchProgress = 0;
      const searchInterval = setInterval(() => {
        if (searchProgress < 90) {
          searchProgress += 5;
          setProgress(searchProgress);
        }
      }, 500);

      const response = await fetch(`${API_URL}/check`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(requestData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      clearInterval(searchInterval);
      setProgress(100);
      setCurrentStep(2);

      const data = await response.json();
      onResultsReceived(data);
    } catch (error) {
      console.error('Error:', error);
      alert('分析过程中出现错误，请重试');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveClaim = (claimToRemove) => {
    setClaims(claims.filter(claim => claim !== claimToRemove));
  };

  const handleCancel = () => {
    setText('');
    setUrl('');
    setClaims([]);
    setShowPreview(false);
    setProgress(0);
    setCurrentStep(0);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-4">
          <div>
            <label htmlFor="textInput" className="block text-sm font-medium text-gray-300">
              输入文本
            </label>
            <textarea
              id="textInput"
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="mt-1 block w-full rounded-md bg-gray-700 border-gray-600 text-gray-300 focus:border-yellow-500 focus:ring-yellow-500"
              rows="4"
              placeholder="请输入要核查的文本内容..."
            />
          </div>
          <div>
            <label htmlFor="urlInput" className="block text-sm font-medium text-gray-300">
              或输入URL
            </label>
            <input
              type="url"
              id="urlInput"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="mt-1 block w-full rounded-md bg-gray-700 border-gray-600 text-gray-300 focus:border-yellow-500 focus:ring-yellow-500"
              placeholder="请输入要核查的网页链接..."
            />
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 disabled:opacity-50"
          >
            {loading ? (
              <>
                <i className="fas fa-spinner fa-spin mr-2" />
                分析中...
              </>
            ) : (
              <>
                <i className="fas fa-search mr-2" />
                分析待核查内容
              </>
            )}
          </button>
        </div>
      </form>

      {/* 进度条 */}
      {loading && (
        <div className="mt-8">
          <div className="relative pt-1">
            <div className="flex mb-2 items-center justify-between">
              <div>
                <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-yellow-600 bg-yellow-200">
                  进度
                </span>
              </div>
              <div className="text-right">
                <span className="text-xs font-semibold inline-block text-yellow-600">
                  {progress}%
                </span>
              </div>
            </div>
            <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-yellow-200">
              <div
                style={{ width: `${progress}%` }}
                className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-yellow-500 transition-all duration-500"
              />
            </div>
          </div>
        </div>
      )}

      {/* 预览区域 */}
      {showPreview && (
        <div className="mt-8">
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-bold text-white mb-4">待核实的点</h2>
            
            <div className="space-y-4 mb-6">
              <div>
                <h3 className="text-lg font-medium text-gray-300 mb-2">原文内容：</h3>
                <div className="bg-gray-700 p-4 rounded-lg text-gray-300">
                  {originalText}
                </div>
              </div>
              
              <div>
                <h3 className="text-lg font-medium text-gray-300 mb-2">待核实的点：</h3>
                <div className="space-y-3">
                  {claims.map((claim, index) => (
                    <ClaimItem
                      key={index}
                      claim={claim}
                      index={index}
                      onRemove={handleRemoveClaim}
                    />
                  ))}
                </div>
              </div>
            </div>

            <div className="flex justify-end space-x-4">
              <button
                onClick={handleCancel}
                className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 focus:outline-none"
              >
                <i className="fas fa-times mr-2" />
                取消
              </button>
              <button
                onClick={handleConfirm}
                className="px-6 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 focus:outline-none"
              >
                <i className="fas fa-check mr-2" />
                确认并继续分析
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FactCheckForm; 