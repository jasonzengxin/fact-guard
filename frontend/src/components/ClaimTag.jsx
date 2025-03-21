import React from 'react';

const ClaimTag = ({ tag }) => {
  const getTagColor = (tag) => {
    switch (tag) {
      case '几乎不可能':
        return 'bg-purple-700 text-white';
      case '可能性较低':
        return 'bg-red-600 text-white';
      case '存疑待考':
        return 'bg-yellow-500 text-gray-900';
      case '非常常见':
        return 'bg-emerald-500 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getTagColor(tag)}`}>
      {tag}
    </span>
  );
};

export default ClaimTag; 