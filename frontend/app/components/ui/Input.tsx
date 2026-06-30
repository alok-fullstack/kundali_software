'use client';

import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  labelHindi?: string;
  error?: string;
}

export function Input({
  label,
  labelHindi,
  error,
  className = '',
  id,
  required,
  ...props
}: InputProps) {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className="mb-4">
      {label && (
        <label
          htmlFor={inputId}
          className="block mb-1.5 font-semibold text-secondary"
        >
          {labelHindi && <span className="mr-1">{labelHindi}</span>}
          ({label})
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <input
        id={inputId}
        className={`
          w-full px-3 py-3
          border-2 border-gray-300 rounded-lg
          text-base font-hindi
          focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500
          disabled:bg-gray-100 disabled:cursor-not-allowed
          ${error ? 'border-red-500' : ''}
          ${className}
        `}
        required={required}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
}
