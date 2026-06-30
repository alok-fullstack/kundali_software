'use client';

import React from 'react';

interface SelectOption {
  value: string | number;
  label: string;
}

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  labelHindi?: string;
  options: SelectOption[];
  error?: string;
}

export function Select({
  label,
  labelHindi,
  options,
  error,
  className = '',
  id,
  required,
  ...props
}: SelectProps) {
  const selectId = id || label?.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className="mb-4">
      {label && (
        <label
          htmlFor={selectId}
          className="block mb-1.5 font-semibold text-secondary"
        >
          {labelHindi && <span className="mr-1">{labelHindi}</span>}
          {label && `(${label})`}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <select
        id={selectId}
        className={`
          w-full px-3 py-3
          border-2 border-gray-300 rounded-lg
          text-base font-hindi
          focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500
          disabled:bg-gray-100 disabled:cursor-not-allowed
          bg-white
          ${error ? 'border-red-500' : ''}
          ${className}
        `}
        required={required}
        {...props}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && (
        <p className="mt-1 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
}
