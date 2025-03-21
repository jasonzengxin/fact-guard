import React from 'react';
import ClaimTag from './ClaimTag';

const ClaimItem = ({ claim, index, onRemove }) => {
  return (
    <div className="flex items-center justify-between p-4 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors">
      <div className="flex items-center space-x-3 flex-1">
        <div className="flex-shrink-0 w-6 h-6 rounded-full bg-yellow-500 flex items-center justify-center text-white font-bold">
          {index + 1}
        </div>
        <div className="flex-1 text-gray-300">
          {claim.claim}
        </div>
        <ClaimTag tag={claim.tag} />
      </div>
      <button
        onClick={() => onRemove(claim)}
        className="ml-4 text-gray-400 hover:text-white focus:outline-none"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  );
};

export default ClaimItem; 